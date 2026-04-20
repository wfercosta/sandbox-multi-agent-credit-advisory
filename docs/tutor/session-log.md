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

### Pendências resolvidas na Sessão 2

- `coverage` adicionado como dependência de desenvolvimento
- Datadog Agent `unhealthy` no cold start documentado no runbook operacional

---

### Próximo passo combinado

**Fase 0, Sessão 2 — Documentação viva e diagrama de contexto**

Objetivo: README raiz navegável, templates de documentação (spec, ADR, runbook, README de pacote) e primeiro diagrama de contexto C4-lite em Mermaid em `docs/diagrams/00-context.md`.

Pré-leitura recomendada: formato MADR para ADRs → https://adr.github.io/madr/

---

### Commits relevantes

| Hash | Mensagem |
|---|---|
| `9f5ca63` | `chore: fase 0 - estrutura do monorepo e tooling` |
| `a2f75b4` | `chore: fase 0 - infraestrutura local` |
| `e70380b` | `docs: adiciona CLAUDE.md com contexto do projeto para Claude Code` |
| `56af79b` | `test: primeiro teste unitário - cálculo SAC em packages/shared` |

---

---

## Fase 0, Sessão 2 — Documentação viva e diagrama de contexto
**Data:** 2026-04-20
**Branch:** `feature/phase0`

---

### O que fizemos

- Refinamento do modelo de interação do sistema: roster de papéis por sessão de discovery (PM, Tech Lead, Frontend, Backend), cada usuário Discord associado a um papel
- Decisão de usar `/discovery setup` como comando estruturado para configurar sessão — separação entre configuração e execução
- Decisão de canal `#discovery-<slug>` como "sala de guerra" (audit trail) + DM para perguntas pontuais aos teammates corretos
- Substituição de Google Drive por **Notion** como destino de entregáveis finais (épicos, features, histórias, SDDs)
- Geração e revisão do `README.md` raiz com estrutura do monorepo, setup local e links de documentação
- Criação manual do diagrama de contexto C4 nível 1 em `docs/diagrams/00-context.md` (Mermaid C4Context)
- Criação manual do template de ADR em `docs/templates/adr.md` (formato MADR estendido com seção de Alternativas consideradas)
- Geração e revisão dos templates `docs/templates/spec.md`, `docs/templates/runbook.md`, `docs/templates/readme-package.md`
- Geração e revisão do runbook operacional `docs/runbooks/infra-local.md` — inclui comportamento do Datadog no cold start, verificação de pgvector, troubleshooting
- Atualização do `.claude/CLAUDE.md`: referência aos templates, esclarecimento do contexto do conhecimento técnico dos agentes (Kotlin/Spring/Next.js refere-se aos produtos analisados, não à stack do sandbox)

---

### Decisões tomadas

| Decisão | Justificativa |
|---|---|
| Roster via `/discovery setup` (opção B) | Separação entre configuração de sessão e execução; input estruturado, validável antes de qualquer LLM ser chamado; PM Agent começa com estado já resolvido |
| Canal `#discovery-<slug>` + DM pontual | Canal é o audit trail natural da sessão; DM mantém a experiência de "agente como colega"; evita dependência de ferramenta externa para reconstruir histórico |
| Notion como destino de entregáveis | Estrutura hierárquica nativa (épico → feature → história) adequada para os artefatos gerados; Google Drive seria repositório de arquivos sem hierarquia de produto |
| MADR estendido com "Alternativas consideradas" | MADR oficial é minimalista demais para decisões de modelo — seção de alternativas acomoda dados experimentais de eval (Fase 3) |
| Conhecimento técnico dos agentes é sobre os produtos analisados | Backend e Frontend agents têm expertise em Kotlin/Spring/Next.js porque é a stack dos produtos do cliente do Itaú, não do sandbox Python |

---

### Pendências

- Notion MCP não está na lista de conectores configurados — necessário configurar antes da Fase 10 quando os agentes publicarem entregáveis
- Hashes dos commits das Sessões 1 e 2 ainda não preenchidos no log — preencher com `git log --oneline`
- Chave de API Anthropic ainda não criada — necessário antes da Fase 2, Sessão 1; budget sugerido: USD 20 de crédito inicial
- `ANTHROPIC_API_KEY=` reservado no `.env` local mas sem valor ainda

---

### Próxima sessão

**Fase 2, Sessão 1 — Claude API direto**

Objetivo: entender o metal antes do LangChain. Messages API, tool use, structured outputs, streaming, prompt caching e extended thinking testados de verdade no contexto do domínio de crédito imobiliário.

Pré-requisitos:
- Chave de API Anthropic criada em https://console.anthropic.com com acesso a Opus, Sonnet e Haiku
- Anotar o tier da conta (Free, Build ou Scale) — afeta rate limits
- `ANTHROPIC_API_KEY` preenchida no `.env` local
- USD 20 de crédito disponível

Pré-leitura recomendada:
- Messages API: https://docs.anthropic.com/en/api/messages
- Prompt caching: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use

---

### Commits relevantes

| Hash | Mensagem |
|---|---|
| `e3321c0` | `doc: adiciona documentação de readme.md e adiciona coverage ao projeto` |
| `8784713` | `docs: adiciona diagrama de contexto C4 nível 1` |
| `a92ad9d` | `docs: adiciona template de ADR no formato MADR estendido` |
| `1bf617b` | `docs: adiciona templates de spec, runbook e readme de pacote` |
| `de20571` | `docs: adiciona runbook de operação da infraestrutura local` |
| `7cbb661` | `docs: referencia templates de documentação no CLAUDE.md` |
| `3e463fe` | `docs: esclarece contexto do conhecimento técnico dos agentes no CLAUDE.md` |
