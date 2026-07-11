# Crucible — Plano de Fases

**Nome do projeto:** Crucible — o cadinho onde uma ideia é pressionada por agentes de IA até sair mais pura, sob autoridade humana.

**Repo:** `marciocandido/crucible` (candidato open source, mesma família de FlowToken e QueueCast)

**CLI:** `crucible`

**Regra permanente (herdada da DEC-09):** cada fase só começa quando a anterior provou valor em uso real. Funcionalidade fora da fase corrente nasce issue, nunca pauta.

---

## Fase 0 — Fundação (imediata)

Renomear tudo que foi decidido como `martec-think` para Crucible. Nenhuma decisão muda de conteúdo.

- `git init` do repo `crucible`
- Consolidação v1 (MOU) + Adendo 01 entram como `docs/` — são os ADRs fundadores
- Teste empírico do RES-10 (CLI do Gemini em modo não interativo lendo o diretório)
- Comandos: `crucible start`, `crucible resume`
- Layout de arquivos conforme RES-12, com `.crucible/` no lugar de `.think/`
- `THINK.md` renomeado para `CRUCIBLE.md` (a lousa)

**Critério de saída:** teste do RES-10 executado e fallback confirmado ou descartado.

## Fase 1 — CLI v1 (o sábado de ~300 linhas)

Implementação integral da especificação congelada: MOU DEC-01 a DEC-10 + Adendo RES-01 a RES-14. Nada além.

**Critério de saída:** 3–4 sessões reais completadas (QueueCast é a primeira), com síntese final gerada e pelo menos uma sessão usando `--auditor` e uma usando `--swap`.

## Fase 2 — Aprendizados e endurecimento

Só existe se a Fase 1 provar valor. Conteúdo vem das issues acumuladas + dor real das sessões. Candidatos já registrados:

- Strip ANSI robusto
- Retry com backoff
- Múltiplas sessões por repo
- `decisions` com autoria/timestamp
- Modos temáticos (`--mode architecture` etc.) se a dor aparecer

**Critério de saída:** o CLI é estável o bastante pra você usar sem pensar na ferramenta.

## Fase 3 — Crucible UI

A fase "bonita e legal". Premissa de design: a UI não substitui o CLI — ela é um cliente do mesmo motor. O core (orquestrador, estado, adapters) vira biblioteca; CLI e UI consomem ela.

### Conceito visual

**A mesa, não o chat.** A metáfora central é a mesa de debate, não uma lista de mensagens:

- **Painel central — a Lousa:** o `CRUCIBLE.md` vivo, renderizado. Decisões, hipóteses e pendências como cards que mudam de coluna em tempo real conforme os agentes emitem blocos `crucible-state`. É o artefato que fica, em primeiro plano — o transcript é secundário.
- **Laterais — os participantes:** cada agente com avatar, papel atual (desenvolvedor/crítico/auditor) e estado (pensando / falou / aguardando). O `--swap` vira arrastar o chapéu de papel de um agente pro outro.
- **Barra do humano — o martelo:** input sempre disponível. Sua mensagem entra com destaque visual de autoridade (a "human_directive" ganha cor própria). Botões do checkpoint: Continuar / Intervir / Aceitar / Encerrar.
- **Timeline do ciclo:** indicador discreto de onde o ciclo está (proposta → crítica → réplica → consolidação → auditoria → você).

### Detalhes que fazem "legal"

- Streaming das respostas em tempo real, com o card do agente pulsando enquanto gera
- Propostas de decisão (RES-04) aparecem como cards pendentes que você confirma com um clique — a confirmação anima o card migrando pra coluna Decidido
- Achados do auditor entram como anotações vermelhas coladas nos cards que eles questionam
- Sessão encerrada gera uma página de síntese compartilhável (o MOU da sessão, exportável em MD/PDF)
- Dark mode primeiro — é ferramenta de quem vive no terminal

### Stack (decisão adiada de propósito)

Provavelmente web local (FastAPI servindo o motor + front Vite), coerente com o padrão MARTEC Core. Mas a stack só se decide no início da Fase 3 — e a discussão de stack da UI é candidata perfeita pra... uma sessão do Crucible sobre o Crucible.

**Critério de saída:** você prefere abrir a UI a abrir o terminal.

## Fase 4 — Ecossistema (horizonte, sem compromisso)

As ideias grandes que viraram issue no MOU voltam aqui como candidatas, não como plano:

- Workspace de Raciocínio / integração com Distill (importar sessões, indexar decisões)
- Sentinel observando sessões (debate longo sem decisão → sugerir encerramento)
- Importação de sessões externas (ChatGPT/Claude/Gemini exports)
- Geração de ADR a partir de sessão aceita

Nenhuma entra sem uma Fase 3 saudável.

---

## Mapa de dependências

```
Fase 0 → Fase 1 → Fase 2 → Fase 3 → Fase 4
  │        │
  │        └── 3-4 sessões reais são o gate de tudo
  └── teste RES-10 é o único bloqueio pré-código
```

*Crucible: as ideias entram brutas, saem forjadas. Autoridade de direção: Márcio.* 🔥
