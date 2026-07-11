# SESSION.md — Exemplo (QueueCast)

> Este é um exemplo preenchido de `SESSION.md`, o contrato de contexto de uma sessão do Crucible (DEC-05). Este arquivo é o único que o humano edita diretamente — nem o orquestrador, nem os agentes escrevem nele. Use como modelo ao iniciar uma sessão real com `crucible start`.

## Objetivo da sessão

Primeira sessão do Crucible, usando QueueCast como cobaia (DEC-10). Questão central: **fila global vs. fila por recurso**, e como o tempo de setup de cada job entra na contabilização do tempo de operação.

## Restrições do Márcio

`[PENDENTE: confirmar com Márcio]` — as restrições específicas para a sessão QueueCast (limites de escopo, coisas fora de cogitação, prazos) não constam nos documentos-fonte desta tarefa. Preencher antes de rodar a sessão real. Exemplo de formato esperado:

- `<restrição 1 — ex.: não considerar migração de dados existentes>`
- `<restrição 2 — ex.: solução deve caber no modelo de workers atual>`

## Decisões já fixadas

`[PENDENTE: confirmar com Márcio]` — decisões prévias do projeto QueueCast relevantes para esta discussão (arquitetura atual de filas, decisões de infraestrutura já tomadas) não constam nos documentos-fonte desta tarefa. Preencher com o conteúdo real de `decisions` de sessões anteriores do QueueCast, se houver, antes de rodar a sessão.

## Hipóteses abertas

- Fila por recurso pode simplificar a priorização, mas multiplica o número de filas a monitorar.
- O tempo de setup pode ser paralelizável fora da fila principal, reduzindo seu peso no tempo total de operação.

> Hipóteses são material de trabalho: qualquer agente pode adicionar ou remover itens desta lista ao longo da sessão, via `hypotheses_add` / `hypotheses_remove` no bloco `crucible-state` (RES-04). Diferente de `decisions`, não exigem confirmação humana para mudar.

## Índice de documentos

Caminhos do repositório QueueCast que os agentes devem priorizar ao ler contexto (RES-11):

- `[PENDENTE: confirmar com Márcio]` — apontar aqui os caminhos reais do repositório QueueCast relevantes para a questão de filas (ex.: módulo de scheduling, configuração de workers, testes de carga existentes).

Exclusões obrigatórias (aplicadas independentemente do índice acima): `.git/`, `node_modules/`, `.venv/`, `dist/`, `build/`, `.env*`, arquivos de credenciais.
