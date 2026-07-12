# Prompt para o Claude Code — Implementação do Crucible

Copie tudo abaixo da linha e cole no Claude Code, na pasta do repo `crucible`.

---

Documentação e planejamento estão prontos. Agora começa a implementação. Você vai trabalhar **issue por issue, na ordem de dependências**, começando pelo M0.

## Regras do jogo (valem para toda a implementação)

1. **Uma issue por vez, um branch por issue, um PR por issue.** Branch: `feat/issue-N-descricao-curta`. PR referencia a issue com `Closes #N`. Não abra a próxima issue antes do PR da atual estar pronto pra minha revisão.
2. **As fontes de verdade são `docs/adr/ADR-001`, `ADR-002` e `docs/protocolo.md`.** Se durante a implementação você encontrar conflito entre o código que quer escrever e um DEC/RES, **pare e me pergunte** — não "interprete". Convenções gerais: `marciocandido/referencias` e o CLAUDE.md deste repo.
3. **DEC-09 vale para o código:** nenhuma função, parâmetro, classe ou abstração além do que a issue pede. Sem "já deixei preparado para o futuro". Preparação para o futuro é acoplamento especulativo — o futuro tem issues próprias.
4. **Critérios de aceite da issue são o contrato do PR.** Cada critério vira um item verificável na descrição do PR, marcado como atendido.
5. **Testes:** pytest para o que é lógica pura (parser do crucible-state, estado, persistência atômica). Adapters e loop podem ter testes com subprocess mockado. Não busque cobertura por vaidade — teste o que quebra caro.
6. **Simplicidade:** stdlib primeiro. Dependências externas só com justificativa de uma linha no PR (Typer/Click para o CLI é aceitável; qualquer coisa além disso, pergunte).

## Ordem de execução

### Agora: #2 — Setup do projeto

Estrutura Python (`src/crucible/`), pyproject.toml, lint (ruff), pytest configurado, entry point `crucible` registrado. PR pequeno e rápido.

### Em seguida: #3 — Teste empírico RES-10 (issue colaborativa)

Esta issue é diferente: **precisa de mim** (autenticação da CLI do Gemini, execução real). Seu papel:

1. Preparar o roteiro de teste: os comandos exatos a rodar, o que observar, os critérios de "lê o filesystem" vs. "precisa de fallback".
2. Me entregar o roteiro e **esperar eu executar e te passar os resultados**.
3. Documentar o resultado em `docs/` e registrar a decisão (acesso nativo confirmado OU fallback do RES-10 ativado).

Não simule nem asuma o resultado deste teste. Ele decide como a issue #18 será implementada.

### Depois: seguir a cadeia

#10 → #11 → #12 → #13 → #14 → (#15, #16, #17 em qualquer ordem) → #18 → #19.

A cada PR aprovado e mergeado, siga para a próxima issue desbloqueada. Se duas estiverem desbloqueadas, prefira a que está no caminho crítico do #14 (o loop é o coração).

### Não é sua: #20 e #21

As issues de M2 (sessões de validação) são minhas — eu executo as sessões. Você para no fim do M1.

## Checkpoint por milestone

Ao fechar o M0 (PRs de #2, #3, #10 mergeados), faça uma pausa e me apresente: estado do repo, o que aprendeu no teste empírico, e qualquer ajuste que sugira nos critérios das issues do M1 **antes** de começá-lo. Mesma coisa ao fechar o M1.

## Começando

Comece agora pela issue #2. Me mostre o plano do PR (arquivos que vai criar, estrutura) em 5 linhas antes de escrever código.

Após abrir cada PR, pare completamente e aguarde minha mensagem. "PR aberto" não é permissão para iniciar a issue seguinte.
