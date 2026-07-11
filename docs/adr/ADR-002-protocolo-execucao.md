# ADR-002 — Protocolo de Execução

**Status:** Aceito
**Data:** 10/07/2026
**Autoridade de direção:** Márcio

Fonte original: `docs/fontes/martec-think-adendo-01.md` (Adendo 01, então nomeado `martec-think`; renomeado para Crucible sem alteração de conteúdo). Complementa ADR-001 — nada aqui altera DEC-01 a DEC-10, apenas os executa.

## Contexto

A consolidação da v1 (ADR-001) definiu o escopo, mas deixou lacunas operacionais: como um ciclo termina, quem tem autoridade sobre o estado, o que acontece quando uma CLI falha, como a sessão persiste em disco. Essas lacunas foram levantadas por GPT (15 itens) e Gemini (4 itens); itens sobrepostos foram unificados nas resoluções abaixo.

## Decisão

**RES-01 — Definição de ciclo:** um ciclo é:

```
desenvolvedor propõe/responde
→ crítico ataca
→ desenvolvedor replica e CONSOLIDA
→ [--auditor] auditor analisa a consolidação
→ humano decide: [c]ontinuar / [i]ntervir / [a]ceitar e encerrar / [q]uit
```

O gatilho mecânico da auditoria é simples: a consolidação é a última seção da réplica do desenvolvedor (RES-03). Exit code 0 + presença do bloco estruturado = consolidação pronta → auditor roda.

**RES-02 — Autoria da consolidação:** quem estiver no papel de **desenvolvedor** consolida, ao fim da própria réplica. Com `--swap`, a responsabilidade acompanha o papel. Não existe quarto papel.

**RES-03 — Contrato de saída dos agentes:** todo turno termina obrigatoriamente com um bloco JSON delimitado:

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

- O texto livre acima do bloco é o conteúdo do debate (vai pro transcript).
- **Só o orquestrador escreve nos arquivos de estado.** Agentes nunca tocam `state.json` ou `CRUCIBLE.md` via filesystem — eles apenas emitem o bloco. Isso elimina parsing heurístico e o risco de um agente corromper o JSON.
- Bloco ausente ou malformado = turno tratado como falha (RES-07).

**RES-04 — Autoridade sobre o estado:** agentes **propõem**, nunca decidem. O campo é `decisions_propose` de propósito: entra numa lista de pendências de confirmação. No checkpoint humano, o script apresenta as propostas e só o que o humano confirmar migra para `decisions`. Hipóteses e perguntas abertas os agentes movimentam livremente — são material de trabalho, não autoridade.

**RES-05 — Auditor só comenta:** o auditor **não emite bloco `crucible-state`**. Sua saída é texto puro (`audit_findings`), anexada ao transcript do ciclo. Incorporar um apontamento é ação do humano ou do desenvolvedor no ciclo seguinte. `[PENDENTE: confirmar com Márcio]` — o Adendo 01 referencia uma "redação do GPT" específica para o prompt do auditor que não está disponível nos documentos-fonte; `docs/prompts/auditor.md` reconstrói o prompt a partir da descrição funcional deste item (papel estritamente analítico, saída obrigatória "Nenhuma inconformidade material encontrada" quando não houver achados) e deve ser validado contra o texto original antes do uso em produção.

**RES-06 — Interrupção humana / SIGINT:**

- **Entre turnos:** o script sempre para no checkpoint e espera comando. Esse é o caminho normal de intervenção.
- **Durante um turno:** SIGINT é capturado pelo orquestrador (handler Python), que encerra o subprocesso da CLI, **descarta a resposta parcial**, preserva o último estado válido e abre o prompt de intervenção. A mensagem humana entra no prompt do próximo turno. String cortada nunca é salva.

**RES-07 — Falha de CLI e timeout:** falha = qualquer um destes: comando não encontrado, exit code ≠ 0, stdout vazio, bloco `crucible-state` ausente/inválido (exceto auditor), timeout excedido.

Comportamento: registra no transcript, **não altera estado**, oferece `[r]epetir / [s]pular / [q]uit`. **Sem retry automático** — gasta token e esconde problema.

Timeout: `--timeout N` com default de 600s por turno.

**RES-08 — Persistência atômica:** estado salvo **após cada turno válido**, via write-temp-and-rename (`state.json.tmp` → `state.json`). Se o turno falhar, o arquivo anterior permanece intacto. Transcript é append-only.

**RES-09 — Adapters de CLI:** três funções, um contrato:

```python
run_claude(prompt, cwd) -> AgentResult
run_codex(prompt, cwd) -> AgentResult
run_gemini(prompt, cwd) -> AgentResult

AgentResult: success, stdout, stderr, exit_code
```

Todas as CLIs rodam em **modo não interativo** (`claude -p`, `codex exec`, equivalente do Gemini), com prompt via argumento/stdin e captura de stdout. Modo não interativo já elimina o problema de ANSI/formatação rica e "Enter fantasma" apontado pelo Gemini — as CLIs em modo print emitem texto puro. Se alguma emitir código ANSI residual, o adapter faz strip (regex de escape codes, uma linha).

**RES-10 — Acesso do Gemini ao filesystem:** pré-requisito de teste antes de codar (única lacuna empírica): verificar se a CLI do Gemini em modo não interativo lê o diretório corrente. Se sim, DEC-04 vale integralmente. Se não, fallback definido: o orquestrador injeta no prompt do auditor o `SESSION.md` + consolidação do ciclo + trechos citados — suficiente para o papel dele, que audita o debate, não o repo inteiro.

**RES-11 — Escopo de leitura do repo:** agentes leem o repositório priorizando os caminhos do índice do `SESSION.md`. Exclusões obrigatórias, declaradas no prompt de sistema de cada agente: `.git/`, `node_modules/`, `.venv/`, `dist/`, `build/`, `.env*`, arquivos de credenciais.

**RES-12 — Layout de arquivos:**

```
SESSION.md          # contrato inicial — só o humano edita
.crucible/
  state.json        # estado operacional — só o orquestrador escreve
  transcript.md     # append-only, tudo que foi dito
CRUCIBLE.md          # lousa: consolidações + síntese final — só o orquestrador escreve
```

Separação clara: contrato / estado / lousa. Ninguém edita `SESSION.md` além do humano — o contrato permanece estável.

**RES-13 — Sessão nova vs. retomada:**

```
crucible start            # nova sessão (erro se .crucible/ existir)
crucible resume           # retoma do último estado válido
```

Sem gestão de múltiplas sessões por repo na v1 — uma sessão ativa por diretório. Sessão paralela? Outra pasta. (Multi-sessão já é issue.)

**RES-14 — Encerramento:** no checkpoint: `[a]` gera a síntese final no `CRUCIBLE.md` (Decidido / Hipóteses / Pendências / Riscos), grava estado e marca a sessão concluída com uma linha no topo do `CRUCIBLE.md`. `[q]` grava estado e sai sem síntese — `resume` continua funcionando.

## Consequências

- O contrato de saída (RES-03) torna o parsing determinístico: o orquestrador nunca precisa interpretar linguagem natural para atualizar estado.
- A separação de autoridade (RES-04) garante que nenhuma decisão entra no registro sem confirmação humana explícita, mesmo que ambos os agentes concordem entre si.
- RES-10 é o único bloqueio empírico antes de começar a Fase 1 (ver `docs/roadmap.md`) — o resultado desse teste determina se o auditor tem acesso pleno ao repositório ou opera apenas sobre o texto injetado no prompt.
- Itens fora de escopo continuam registrados como candidatos a issue: strip ANSI robusto (além do regex de uma linha do RES-09), múltiplas sessões por repositório, retry automático com backoff, `decisions` com autoria/timestamp estruturados.
