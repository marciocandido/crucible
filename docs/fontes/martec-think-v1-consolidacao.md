# martec-think — Consolidação Final da v1

**Status:** DECIDIDO. Esta é a especificação fechada da v1, definida por Márcio (autoridade de direção). A partir daqui, discutimos apenas **lacunas** desta especificação. Qualquer funcionalidade, camada, entidade ou requisito além do listado **nasce como issue** — não entra na v1, não vira debate.

---

## O que é

Um script CLI que orquestra um debate técnico turn-based entre agentes de IA sobre uma ideia do Márcio, com ele participando no meio do loop. Não é produto, não é plataforma. É uma ferramenta descartável até provar valor em 3–4 sessões reais.

## Decisões fechadas

**DEC-01 — Formato do debate:** turn-based, sequencial, síncrono. Claude propõe → Codex critica → Claude responde → ciclo se repete. Sem concorrência, sem execução paralela de agentes.

**DEC-02 — Dois agentes no loop + auditor opcional:** Claude (desenvolvedor estrutural) e Codex (crítico técnico) formam o loop principal. Gemini entra como **auditor**, via flag `--auditor`, executado **uma vez por ciclo**, após a consolidação — nunca a cada fala. Papel do auditor é estritamente analítico: afirmações sem lastro, contradições, premissas tratadas como decisões. Não gera solução, não propõe arquitetura.

**DEC-03 — Troca de papéis:** flag `--swap` inverte quem desenvolve e quem critica. Serve para testar qual configuração rende mais nas primeiras sessões.

**DEC-04 — Contexto via repo físico:** o script roda dentro do repositório do projeto em discussão. Os agentes usam acesso nativo ao filesystem das próprias CLIs (Claude Code, Codex CLI). **Sem MCP, sem RAG, sem banco vetorial.**

**DEC-05 — `SESSION.md` como contrato de contexto:** arquivo único na raiz com: objetivo da sessão, restrições do Márcio, decisões já fixadas, hipóteses abertas, e índice apontando para os demais documentos do repo. Todo agente recebe este arquivo no prompt inicial e busca o resto sob demanda.

**DEC-06 — Estado da sessão:** JSON simples em disco com três listas: `decisions`, `hypotheses`, `open_questions`. Sem Pydantic patch protocol, sem versionamento de estado, sem event queue.

**DEC-07 — Intervenção humana:** Márcio interrompe quando quiser (Ctrl+C ou equivalente), digita, e sua mensagem tem precedência sobre o rumo do debate. Mudança relevante de direção só parte do humano.

**DEC-08 — Saída:** sessão salva em Markdown, contendo: Decidido, Hipóteses, Pendências, Riscos, transcript. O Markdown **é** a lousa compartilhada da v1.

**DEC-09 — Regra anti-expansão (vale para o debate E para esta ferramenta):** nada que não seja consequência direta da ideia em discussão entra na proposta principal. Possibilidades adicionais são marcadas como opcionais ou viram issue.

**DEC-10 — Primeira cobaia:** QueueCast. Primeira questão de sessão: fila global vs. fila por recurso, e como setup entra no tempo de operação.

## O que explicitamente NÃO está na v1 (já são issues, não pauta)

- Integração com Git / geração automática de ADR
- FastAPI, orquestrador como serviço, qualquer servidor
- Qdrant, embeddings, RAG, índice factual em duas camadas
- Parâmetro genérico `--agents N`
- Importação de sessões externas (ChatGPT/Claude/Gemini exports)
- Workspace de Raciocínio / módulo do Distill
- Sentinel observando sessões
- Modos temáticos (`--mode architecture` etc.)
- Fila de eventos com prioridades e invalidação de runs

## O que se espera de cada participante agora

Apontar **lacunas desta especificação** — algo que impeça a v1 de rodar como descrita. Exemplos válidos: "como o script sabe que o ciclo terminou?", "o que acontece se uma CLI falhar no meio do turno?". Exemplos inválidos: qualquer proposta que comece com "seria interessante também...".

---

*Consolidado em 10/07/2026. Autoridade de direção: Márcio. Escopo congelado por decreto — e ele venceu.* 🙃
