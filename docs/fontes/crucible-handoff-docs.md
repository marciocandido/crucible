# Crucible — Handoff: Geração da Documentação Inicial

**Para:** o agente encarregado (Claude Code ou Codex CLI, à escolha do Márcio)
**Tarefa:** gerar a documentação inicial do repositório `marciocandido/crucible` a partir dos três documentos-fonte anexados. **Não implementar código nesta tarefa.**

## Documentos-fonte (leitura obrigatória, nesta ordem)

1. `martec-think-v1-consolidacao.md` — o MOU: DEC-01 a DEC-10 (escopo congelado da v1)
2. `martec-think-adendo-01.md` — RES-01 a RES-14 (protocolo de execução)
3. `crucible-fases.md` — plano de fases e conceito da UI

**Nota de renomeação:** os dois primeiros documentos usam o nome antigo `martec-think`. O projeto agora chama **Crucible**. Na documentação gerada, aplicar: `martec-think` → `crucible` (CLI), `.think/` → `.crucible/`, `THINK.md` → `CRUCIBLE.md`, bloco ` ```martec-state ` → ` ```crucible-state `. O conteúdo das decisões não muda.

## Estrutura a gerar

```
crucible/
├── README.md
├── CLAUDE.md
├── AGENTS.md
├── docs/
│   ├── adr/
│   │   ├── ADR-001-escopo-v1.md
│   │   └── ADR-002-protocolo-execucao.md
│   ├── roadmap.md
│   ├── protocolo.md
│   └── prompts/
│       ├── desenvolvedor.md
│       ├── critico.md
│       └── auditor.md
└── SESSION.example.md
```

## Especificação por arquivo

**README.md** — Em inglês (candidato open source). O que é o Crucible (mesa de debate entre agentes de IA sob autoridade humana), o problema que resolve, o loop turn-based em diagrama ASCII, quickstart (`crucible start` / `resume`), flags (`--swap`, `--auditor`, `--timeout`), layout de arquivos gerados, status do projeto (Fase 0). Tom direto, sem marketing.

**CLAUDE.md e AGENTS.md** — Convenções do repo para agentes de código. Apontar `marciocandido/referencias` como fonte de convenções (padrão dos repos do Márcio). Regra central destacada: DEC-09 (anti-expansão) vale para quem implementa — funcionalidade fora da fase corrente vira issue, nunca código.

**docs/adr/ADR-001** — Conversão do MOU em formato ADR (Contexto / Decisão / Consequências). Preservar DEC-01..10 numerados e a lista "explicitamente fora da v1".

**docs/adr/ADR-002** — Conversão do Adendo em ADR. Preservar RES-01..14 numerados.

**docs/roadmap.md** — Adaptação direta do `crucible-fases.md`, com critérios de saída por fase.

**docs/protocolo.md** — O documento operacional: anatomia de um ciclo (RES-01), contrato do bloco `crucible-state` (RES-03) com exemplo válido e inválido, regras de autoridade (RES-04/05), semântica de falha, timeout e SIGINT (RES-06/07), persistência (RES-08), contrato dos adapters (RES-09).

**docs/prompts/*.md** — Os três prompts de papel, prontos para uso pelo orquestrador:
- `desenvolvedor.md`: estruturar a ideia, explicitar pressupostos, responder críticas, consolidar ao fim do turno, emitir bloco `crucible-state`. Proibido expandir escopo (DEC-09 no prompt).
- `critico.md`: atacar lacunas, dependências ocultas, inconsistências operacionais. Proibido propor arquitetura alternativa completa. Emite bloco `crucible-state`.
- `auditor.md`: usar a redação do GPT registrada no Adendo (RES-05) — papel estritamente analítico, sem bloco de estado, saída obrigatória "Nenhuma inconformidade material encontrada" quando aplicável.

**SESSION.example.md** — Exemplo preenchido com a sessão QueueCast (DEC-10): objetivo (fila global vs. por recurso; setup no tempo de operação), restrições, decisões prévias relevantes do QueueCast, índice de documentos.

## Regras para o agente executor

1. **Não inventar decisões.** Toda afirmação técnica na documentação deve rastrear para um DEC-* ou RES-*. Na dúvida, marcar como `[PENDENTE: confirmar com Márcio]`.
2. **Não implementar.** Esta tarefa termina em documentação. O código é a tarefa seguinte, em PR separado.
3. **Idiomas:** README em inglês; demais documentos em português (público interno primeiro; tradução é issue futura).
4. **Entregar como PR único** (`docs: initial documentation`) seguindo o fluxo de duas fases já usado no Sentinel: docs primeiro, milestones/issues depois.
5. Ao final, listar as issues que devem ser criadas: as já registradas no MOU/Adendo + `[Fase 0] Teste empírico RES-10 — CLI Gemini em modo não interativo`.

---

*Handoff emitido em 10/07/2026. Autoridade de direção: Márcio.*
