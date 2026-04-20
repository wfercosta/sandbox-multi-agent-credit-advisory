# Session Log — Tutor de Sistemas Multi-Agentes

## Fase 0, Sessão 1 — Fundação do monorepo
**Data:** 2026-04-19
**Branch:** `feature/phase0`

---

### O que fizemos

- Criação manual da estrutura de diretórios do monorepo (`apps/`, `packages/`, `infra/`, `docs/`, `.claude/`, `.github/`)
- Configuração do `pyproject.toml` raiz com `uv` workspaces, membros explícitos por pacote
- Configuração de tooling: `ruff` (lint + format), `pyright` (type checking), `pytest` com `asyncio_mode=auto`
- Configuração do `pre-commit` com hooks de ruff, mypy, trailing whitespace, end-of-file, check-yaml, check-toml e proteção da branch main
- Branch protection no GitHub: PR obrigatório para merge na `main`, bloqueio de force push e deleção
- Infraestrutura local via `podman-compose`: Postgres 17 + pgvector e Datadog Agent 7
- Script de inicialização da extensão `vector` no Postgres (`infra/docker/init/01-extensions.sql`)
- Redação do `.claude/CLAUDE.md` com contexto do projeto, domínio, stack, convenções e restrições para o Claude Code
- Primeiro teste unitário em `packages/shared/tests/test_math.py` — cálculo de parcelas SAC com `Decimal`

---

### Decisões tomadas

| Decisão | Justificativa |
|---|---|
| Python 3.13 | Versão instalada no ambiente; LangChain/LangGraph compatíveis; free-threaded não habilitado |
| `uv` workspaces com membros explícitos | Globs genéricos (`packages/*`) capturam diretórios agrupadores sem `pyproject.toml` |
| `podman` no lugar de `docker` | Preferência do ambiente local; drop-in replacement para compose |
| `asyncio_mode = "auto"` no pytest | Elimina boilerplate de `@pytest.mark.asyncio` — padrão para projeto majoritariamente async |
| `pytest.raises` sempre com tipo e `match=` | `pytest.raises(Exception)` gera falsos positivos — lição aprendida no teste SAC |
| Skills do produto embarcadas em `packages/agents/<agent>/skills/` | Ciclo de vida diferente das skills do Claude Code em `.claude/skills/` |
| Terraform e Kubernetes fora do `CLAUDE.md` por ora | Chegam na Fase 12 — versões fixas agora criariam documento desatualizado antes do uso |

---

### Pendências

- `packages/shared` é o único membro do workspace com código real — os demais têm `pyproject.toml` mínimo vazio. Cada pacote ganha conteúdo na fase correspondente.
- `coverage` listado nos comandos do `CLAUDE.md` mas não adicionado como dependência ainda — adicionar quando a suite crescer.
- Datadog Agent inicializa com `unhealthy` nos primeiros ~60s no Podman — comportamento esperado, documentar no runbook operacional na Sessão 2.

---

### Próximo passo combinado

**Fase 0, Sessão 2 — Documentação viva e diagrama de contexto**

Objetivo: README raiz navegável, templates de documentação (spec, ADR, runbook, README de pacote) e primeiro diagrama de contexto C4-lite em Mermaid em `docs/diagrams/00-context.md`.

Pré-leitura recomendada: formato MADR para ADRs → https://adr.github.io/madr/

---

### Commits relevantes

| Hash | Mensagem |
|---|---|
| a ser preenchido com `git log --oneline` | `chore: fase 0 - estrutura do monorepo e tooling` |
| a ser preenchido com `git log --oneline` | `chore: fase 0 - infraestrutura local` |
| a ser preenchido com `git log --oneline` | `docs: adiciona CLAUDE.md com contexto do projeto para Claude Code` |
| a ser preenchido com `git log --oneline` | `test: primeiro teste unitário - cálculo SAC em packages/shared` |
