# Protocolo de Execução do Crucible

Este documento descreve o funcionamento operacional do orquestrador Crucible, consolidando as resoluções de `docs/adr/ADR-002-protocolo-execucao.md` em formato de referência de implementação. Nenhuma regra aqui é nova — cada seção rastreia para um ou mais `RES-*`.

## Anatomia de um ciclo (RES-01)

```
desenvolvedor propõe/responde
→ crítico ataca
→ desenvolvedor replica e CONSOLIDA
→ [--auditor] auditor analisa a consolidação
→ humano decide: [c]ontinuar / [i]ntervir / [a]ceitar e encerrar / [q]uit
```

A consolidação é sempre a última seção da réplica do desenvolvedor. O gatilho para rodar o auditor (quando `--auditor` está ativo) é mecânico: exit code `0` da CLI do desenvolvedor **e** presença de um bloco `crucible-state` válido na saída. Não há interpretação semântica do conteúdo — é uma checagem estrutural.

A autoria da consolidação segue o papel, não o agente: quem estiver como **desenvolvedor** consolida no fim da própria réplica. Com `--swap`, a responsabilidade migra junto com o papel (RES-02). Não existe um quarto papel para essa função.

## Contrato do bloco `crucible-state` (RES-03)

Todo turno de desenvolvedor ou crítico termina obrigatoriamente com um bloco JSON delimitado por uma cerca de código com o marcador `crucible-state`:

````
```crucible-state
{
  "decisions_propose": [],
  "hypotheses_add": [],
  "hypotheses_remove": [],
  "open_questions_add": [],
  "open_questions_resolve": []
}
```
````

Regras:

- Tudo que aparece **acima** do bloco no output do agente é texto livre — o conteúdo do debate — e vai para `transcript.md`.
- **Só o orquestrador escreve nos arquivos de estado** (`state.json`, `CRUCIBLE.md`). Os agentes nunca tocam esses arquivos via filesystem; eles apenas emitem o bloco, e é o orquestrador quem interpreta e persiste.
- Bloco ausente ou malformado (JSON inválido, chaves faltando) é tratado como falha de turno (ver seção de falhas abaixo) — exceto para o auditor, que nunca emite esse bloco (RES-05).

### Exemplo válido

````
```crucible-state
{
  "decisions_propose": ["Fila por recurso, não global — cada tipo de trabalho tem sua fila"],
  "hypotheses_add": ["Setup de cada job pode ser paralelizado fora da fila principal"],
  "hypotheses_remove": [],
  "open_questions_add": ["Como o operador prioriza filas quando há concorrência entre recursos?"],
  "open_questions_resolve": []
}
```
````

### Exemplo inválido

````
```crucible-state
{
  "decisions_propose": ["Fila por recurso"],
  "hypotheses_add": ["Setup pode ser paralelizado"]
  // faltam hypotheses_remove, open_questions_add, open_questions_resolve
}
```
````

Inválido por dois motivos independentes, cada um suficiente para reprovar o turno: (1) comentário `//` não é JSON válido; (2) chaves obrigatórias do contrato estão ausentes.

## Autoridade sobre o estado (RES-04, RES-05)

- **Decisões:** agentes **propõem**, nunca decidem. O campo `decisions_propose` alimenta uma lista de pendências de confirmação. No checkpoint humano, o orquestrador apresenta as propostas do ciclo; apenas o que o humano confirmar migra para `decisions` em `state.json`.
- **Hipóteses e perguntas abertas:** são material de trabalho, não de autoridade — os agentes movimentam essas listas livremente via `hypotheses_add`/`hypotheses_remove` e `open_questions_add`/`open_questions_resolve`, sem necessidade de confirmação humana.
- **Auditor:** não emite bloco `crucible-state`. Sua saída é texto puro (`audit_findings`), anexado ao transcript do ciclo. Papel estritamente analítico — aponta afirmações sem lastro, contradições e premissas tratadas como decisões; não propõe solução nem arquitetura. Incorporar um apontamento do auditor é sempre ação do humano, ou do desenvolvedor no ciclo seguinte. Ver `docs/prompts/auditor.md` para o prompt correspondente e a nota de `[PENDENTE]` associada.

## Falha, timeout e SIGINT (RES-06, RES-07)

### Falha de turno

Um turno é considerado falho se qualquer uma destas condições ocorrer:

- comando da CLI não encontrado;
- exit code diferente de 0;
- stdout vazio;
- bloco `crucible-state` ausente ou inválido (não se aplica ao turno do auditor, que não emite esse bloco);
- timeout excedido.

Comportamento em caso de falha: o orquestrador registra o ocorrido no transcript, **não altera o estado** (`state.json` permanece no último valor válido) e oferece três opções ao humano: `[r]epetir`, `[s]pular`, `[q]uit`. Não há retry automático — retry automático gasta token e esconde o problema em vez de expô-lo.

### Timeout

Cada turno tem um timeout configurável via `--timeout N` (segundos), com default de **600s**.

### SIGINT

- **Entre turnos:** o orquestrador sempre para no checkpoint humano e espera comando — esse é o caminho normal de intervenção, sem necessidade de sinal.
- **Durante um turno:** o SIGINT é capturado pelo orquestrador (handler no processo Python), que:
  1. encerra o subprocesso da CLI em execução;
  2. **descarta a resposta parcial** — nenhuma string cortada é salva em transcript ou estado;
  3. preserva o último estado válido conhecido;
  4. abre o prompt de intervenção humana.
  A mensagem digitada pelo humano nesse momento entra no prompt do próximo turno.

## Persistência (RES-08)

O estado é salvo em `state.json` **após cada turno válido**, usando o padrão write-temp-and-rename: escreve em `state.json.tmp` e só então renomeia para `state.json`. Se o turno falhar, o arquivo de estado anterior permanece intacto — nunca há um `state.json` parcialmente escrito.

`transcript.md` é append-only: cada turno (incluindo falhas registradas) acrescenta conteúdo, nunca reescreve o que já existe.

## Contrato dos adapters (RES-09)

Três funções, um contrato único:

```python
run_claude(prompt, cwd) -> AgentResult
run_codex(prompt, cwd) -> AgentResult
run_gemini(prompt, cwd) -> AgentResult

AgentResult: success, stdout, stderr, exit_code
```

Todas as CLIs rodam em **modo não interativo** (`claude -p`, `codex exec`, e o equivalente não interativo do Gemini), recebendo o prompt via argumento ou stdin e tendo o stdout capturado pelo orquestrador. O modo não interativo já elimina, por construção, o problema de códigos ANSI e "Enter fantasma": CLIs em modo print emitem texto puro. Caso alguma CLI emita código ANSI residual mesmo assim, o adapter correspondente faz o strip via uma única expressão regular de escape codes.

## Acesso ao filesystem e escopo de leitura (RES-10, RES-11)

O pré-requisito empírico antes de iniciar a implementação da Fase 1 é verificar se a CLI do Gemini, em modo não interativo, lê o diretório corrente (DEC-04 pressupõe que sim para todos os agentes). Se confirmado, todos os três agentes acessam o repositório nativamente. Se não confirmado, o fallback é injetar no prompt do auditor o conteúdo de `SESSION.md`, a consolidação do ciclo corrente e trechos citados no debate — suficiente para o papel estritamente analítico do auditor, que audita o debate e não o repositório inteiro.

Independentemente do resultado do teste, todos os agentes priorizam, ao ler o repositório, os caminhos listados no índice de `SESSION.md`. Exclusões obrigatórias, declaradas no prompt de sistema de cada agente: `.git/`, `node_modules/`, `.venv/`, `dist/`, `build/`, `.env*` e arquivos de credenciais.

## Layout de arquivos (RES-12)

```
SESSION.md          # contrato inicial — só o humano edita
.crucible/
  state.json        # estado operacional — só o orquestrador escreve
  transcript.md     # append-only, tudo que foi dito
CRUCIBLE.md          # lousa: consolidações + síntese final — só o orquestrador escreve
```

## Início e retomada de sessão (RES-13)

```
crucible start            # nova sessão — erro se .crucible/ já existir
crucible resume           # retoma do último estado válido em .crucible/state.json
```

A v1 não gerencia múltiplas sessões por repositório: há no máximo uma sessão ativa por diretório. Uma sessão paralela requer outro diretório.

## Encerramento (RES-14)

No checkpoint humano, ao final de um ciclo:

- `[a]` (aceitar e encerrar): gera a síntese final no `CRUCIBLE.md` (seções Decidido / Hipóteses / Pendências / Riscos), grava o estado final e marca a sessão como concluída com uma linha no topo do `CRUCIBLE.md`.
- `[q]` (quit): grava o estado corrente e sai sem gerar síntese. `crucible resume` continua funcionando normalmente a partir desse ponto.
