# martec-think — Adendo 01: Resolução de Lacunas

**Status:** DECIDIDO. Complementa a Consolidação v1. As lacunas apontadas por GPT (15 itens) e Gemini (4 itens) foram absorvidas abaixo. Itens sobrepostos foram unificados. Nada aqui altera DEC-01 a DEC-10 — apenas as executa.

---

## RES-01 — Definição de ciclo (GPT#1, Gemini#4)

Um ciclo é:

```
desenvolvedor propõe/responde
→ crítico ataca
→ desenvolvedor replica e CONSOLIDA
→ [--auditor] auditor analisa a consolidação
→ humano decide: [c]ontinuar / [i]ntervir / [a]ceitar e encerrar / [q]uit
```

O gatilho mecânico da auditoria é simples: a consolidação é a última seção da réplica do desenvolvedor (ver RES-03). Exit code 0 + presença do bloco estruturado = consolidação pronta → auditor roda.

## RES-02 — Autoria da consolidação (GPT#2)

Quem estiver no papel de **desenvolvedor** consolida, ao fim da própria réplica. Com `--swap`, a responsabilidade acompanha o papel. Não existe quarto papel.

## RES-03 — Contrato de saída dos agentes (GPT#4, Gemini#2)

Todo turno termina obrigatoriamente com um bloco JSON delimitado:

````
```martec-state
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
- **Só o orquestrador escreve nos arquivos de estado.** Agentes nunca tocam `state.json` ou `THINK.md` via filesystem — eles apenas emitem o bloco. Isso resolve a Lacuna 2 do Gemini na raiz: zero parsing heurístico, zero risco de agente corromper JSON.
- Bloco ausente ou malformado = turno tratado como falha (RES-07).

## RES-04 — Autoridade sobre o estado (GPT#5)

Agentes **propõem**, nunca decidem. O campo é `decisions_propose` de propósito: entra numa lista de pendências de confirmação. No checkpoint humano, o script apresenta as propostas e só o que Márcio confirmar migra para `decisions`. Hipóteses e perguntas abertas os agentes movimentam livremente — são material de trabalho, não autoridade.

## RES-05 — Auditor só comenta (GPT#3)

O auditor **não emite bloco `martec-state`**. Sua saída é texto puro (`audit_findings`), anexada ao transcript do ciclo. Incorporar um apontamento é ação do humano ou do desenvolvedor no ciclo seguinte. Prompt do auditor conforme redação do GPT, incluindo a saída obrigatória "Nenhuma inconformidade material encontrada" quando não houver achados.

## RES-06 — Interrupção humana / SIGINT (GPT#6, Gemini#3)

- **Entre turnos:** o script sempre para no checkpoint e espera comando. Esse é o caminho normal de intervenção.
- **Durante um turno:** SIGINT é capturado pelo orquestrador (handler Python), que encerra o subprocesso da CLI, **descarta a resposta parcial**, preserva o último estado válido e abre o prompt de intervenção. A mensagem humana entra no prompt do próximo turno. String cortada nunca é salva.

## RES-07 — Falha de CLI e timeout (GPT#8, GPT#9)

Falha = qualquer um destes: comando não encontrado, exit code ≠ 0, stdout vazio, bloco `martec-state` ausente/inválido (exceto auditor), timeout excedido.

Comportamento: registra no transcript, **não altera estado**, oferece `[r]epetir / [s]pular / [q]uit`. **Sem retry automático** — gasta token e esconde problema.

Timeout: `--timeout N` com default de 600s por turno.

## RES-08 — Persistência atômica (GPT#7)

Estado salvo **após cada turno válido**, via write-temp-and-rename (`state.json.tmp` → `state.json`). Se o turno falhar, o arquivo anterior permanece intacto. Transcript é append-only.

## RES-09 — Adapters de CLI (GPT#10, Gemini#1)

Três funções, um contrato:

```python
run_claude(prompt, cwd) -> AgentResult
run_codex(prompt, cwd) -> AgentResult
run_gemini(prompt, cwd) -> AgentResult

AgentResult: success, stdout, stderr, exit_code
```

Todas as CLIs rodam em **modo não interativo** (`claude -p`, `codex exec`, equivalente do Gemini), com prompt via argumento/stdin e captura de stdout. Modo não interativo já elimina o problema de ANSI/formatação rica e "Enter fantasma" apontado pelo Gemini — as CLIs em modo print emitem texto puro. Se alguma emitir código ANSI residual, o adapter faz strip (regex de escape codes, uma linha).

## RES-10 — Acesso do Gemini ao filesystem (GPT#11)

**Pré-requisito de teste antes de codar** (única lacuna empírica): verificar se a CLI do Gemini em modo não interativo lê o diretório corrente. Se sim, DEC-04 vale integralmente. Se não, fallback definido: o orquestrador injeta no prompt do auditor o `SESSION.md` + consolidação do ciclo + trechos citados — suficiente para o papel dele, que audita o debate, não o repo inteiro.

## RES-11 — Escopo de leitura do repo (GPT#12)

Agentes leem o repositório priorizando os caminhos do índice do `SESSION.md`. Exclusões obrigatórias, declaradas no prompt de sistema de cada agente: `.git/`, `node_modules/`, `.venv/`, `dist/`, `build/`, `.env*`, arquivos de credenciais.

## RES-12 — Layout de arquivos (GPT#14)

```
SESSION.md          # contrato inicial — só o humano edita
.think/
  state.json        # estado operacional — só o orquestrador escreve
  transcript.md     # append-only, tudo que foi dito
THINK.md            # lousa: consolidações + síntese final — só o orquestrador escreve
```

Separação clara: contrato / estado / lousa. Ninguém edita `SESSION.md` além do humano — o contrato permanece estável.

## RES-13 — Sessão nova vs. retomada (GPT#13)

```
martec-think start            # nova sessão (erro se .think/ existir)
martec-think resume           # retoma do último estado válido
```

Sem gestão de múltiplas sessões por repo na v1 — uma sessão ativa por diretório. Sessão paralela? Outra pasta. (Multi-sessão já é issue.)

## RES-14 — Encerramento (GPT#15)

No checkpoint: `[a]` gera a síntese final no `THINK.md` (Decidido / Hipóteses / Pendências / Riscos), grava estado e marca a sessão concluída com uma linha no topo do `THINK.md`. `[q]` grava estado e sai sem síntese — `resume` continua funcionando.

---

## Registro de issues nascidas neste adendo

- Strip ANSI robusto se alguma CLI se comportar mal em modo print
- Múltiplas sessões por repositório
- Retry automático com backoff
- `decisions` com autoria/timestamp estruturados

---

*Adendo consolidado em 10/07/2026. As lacunas de protocolo estão fechadas. Próximo passo não é mais discussão: é `git init` e o teste empírico do RES-10.* 🔩
