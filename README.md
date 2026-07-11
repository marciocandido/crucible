# Crucible

Crucible is a CLI that runs a turn-based technical debate between AI agents about an idea, with a human in the loop deciding what actually sticks.

It is not a product and not a platform. It is a disposable tool until it proves value across 3–4 real sessions.

## The problem

Bouncing an idea off a single AI agent tends to produce agreement, not pressure-testing. Crucible forces a structured adversarial pass: one agent builds the idea, another attacks it, and nothing becomes a decision until a human confirms it. The idea goes in raw and comes out forged — or it doesn't survive, which is also useful information.

## How it works

Two agents run the main loop — one in a developer role, one in a critic role — with an optional third agent auditing the outcome of each cycle. Roles can be swapped. A human sits at the checkpoint between cycles and has final authority over direction and over which proposals become decisions.

```
developer proposes / responds
       │
       ▼
   critic attacks
       │
       ▼
developer replies and CONSOLIDATES
       │
       ▼
[--auditor] auditor analyzes the consolidation
       │
       ▼
human decides: [c]ontinue / [i]ntervene / [a]ccept and close / [q]uit
```

Agents run their native CLIs (Claude Code, Codex CLI, and optionally Gemini CLI) in non-interactive mode against the project repository on disk — no MCP, no RAG, no vector database. Every turn ends with a structured state block; only the orchestrator ever writes to disk. Agents propose, they never decide.

## Quickstart

```
crucible start      # new session (errors if .crucible/ already exists)
crucible resume      # resume from the last valid state
```

## Flags

| Flag | Effect |
|---|---|
| `--swap` | Inverts which agent develops and which critiques |
| `--auditor` | Runs a third agent as auditor once per cycle, after consolidation |
| `--timeout N` | Per-turn timeout in seconds (default: 600) |

## File layout

```
SESSION.md          # session contract — edited only by the human
.crucible/
  state.json        # operational state — written only by the orchestrator
  transcript.md      # append-only log of everything said
CRUCIBLE.md          # the board: consolidations and final synthesis — written only by the orchestrator
```

## Status

**Phase 0 — Foundation.** This repository currently contains documentation only; no code has been implemented yet. See [`docs/roadmap.md`](docs/roadmap.md) for the phase plan and [`docs/adr/`](docs/adr) for the decisions this project is built on.

## Documentation

- [`docs/adr/ADR-001-escopo-v1.md`](docs/adr/ADR-001-escopo-v1.md) — v1 scope decisions
- [`docs/adr/ADR-002-protocolo-execucao.md`](docs/adr/ADR-002-protocolo-execucao.md) — execution protocol decisions
- [`docs/roadmap.md`](docs/roadmap.md) — phase plan
- [`docs/protocolo.md`](docs/protocolo.md) — operational protocol (cycle anatomy, state contract, failure handling)
- [`docs/prompts/`](docs/prompts) — role prompts for the orchestrator
- [`SESSION.example.md`](SESSION.example.md) — example session contract
