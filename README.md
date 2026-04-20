# sandbox-multi-agent-credit-advisory

Sistema multi-agente para product discovery no domínio de crédito imobiliário brasileiro. Um PM Agent conduz o processo de descoberta via Discord com human-in-the-loop; agentes técnicos (Tech Lead, Frontend, Backend) recebem o output do PM e produzem artefatos como PRDs, backlog refinado e Software Design Documents. Toda a lógica de domínio é fundamentada em regulação rastreável (BACEN, CMN, Lei 9.514/97).

## Estrutura do repositório

```
.
├── apps/
│   ├── discord-bot/        # Bot Discord — interface de interação human-in-the-loop
│   ├── orchestrator/       # Orquestrador principal do grafo de agentes
│   └── teams-bot/          # Bot Microsoft Teams (alternativa ao Discord)
├── packages/
│   ├── agents/             # Agentes especializados: pm, tech_lead, backend, frontend
│   ├── mcp-servers/        # MCP Servers expostos para consumo dos agentes
│   ├── memory/             # Integração com armazenamento e busca de memórias
│   ├── models/             # Wrappers de interação com modelos Anthropic
│   ├── observability/      # Instrumentação Datadog (traces, métricas, logs)
│   ├── rag/                # Pipeline de RAG sobre o corpus regulatório
│   ├── shared/             # Schemas Pydantic, utilitários e configuração compartilhada
│   └── tools/              # Ferramentas reutilizáveis pelos agentes
├── infra/
│   ├── docker/             # Compose local: Postgres 17 + pgvector, Datadog Agent
│   ├── k8s/                # Manifestos Kubernetes
│   ├── argocd/             # Configuração GitOps ArgoCD
│   └── terraform/          # Infraestrutura como código (IaC)
├── docs/
│   ├── adr/                # Architecture Decision Records (formato MADR)
│   ├── diagrams/           # Diagramas de arquitetura e solução (Mermaid)
│   ├── playbooks/          # Melhores práticas e estratégias técnicas padronizadas
│   ├── runbooks/           # Procedimentos operacionais
│   └── templates/          # Templates reutilizáveis de documentação
├── specs/                  # Especificações de features (specs/NNNN-slug/spec.md)
└── .claude/                # Instruções e agentes customizados para Claude Code
```

## Configuração do ambiente local

### Pré-requisitos

- Python 3.13
- [uv](https://docs.astral.sh/uv/) — gerenciador de pacotes e workspaces
- [podman](https://podman.io/) + [podman-compose](https://github.com/containers/podman-compose) — containers locais

### Instalação

```bash
git clone https://github.com/wfercosta/sandbox-multi-agent-credit-advisory.git
cd sandbox-multi-agent-credit-advisory

# Instala todas as dependências do workspace
uv sync
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do repositório com as seguintes variáveis:

```bash
POSTGRES_USER=credit_advisory
POSTGRES_PASSWORD=credit_advisory
POSTGRES_DB=credit_advisory
DD_API_KEY=<chave-do-datadog>
DD_SITE=datadoghq.com
```

### Infraestrutura local

```bash
# Sobe Postgres 17 + pgvector e Datadog Agent em modo detached
podman-compose -f infra/docker/compose.yaml --env-file .env up -d

# Para os containers
podman-compose -f infra/docker/compose.yaml down
```

### Testes

```bash
# Suite completa
uv run pytest

# Suite de um pacote específico
uv run pytest packages/shared

# Com cobertura
uv run coverage run -m pytest
uv run coverage report
```

### Lint e formatação

```bash
uv run ruff check .          # verifica o projeto inteiro
uv run ruff check --fix .    # corrige automaticamente
uv run ruff format .         # formata todos os arquivos
```

### Verificação de tipos

```bash
uv run pyright               # verifica todo o projeto
uv run pyright packages/shared  # verifica pacote específico
```

## Documentação

| Recurso | Localização |
|---|---|
| Instruções para Claude Code | [.claude/CLAUDE.md](.claude/CLAUDE.md) |
| Diagramas de arquitetura | [docs/diagrams/](docs/diagrams/) |
| Architecture Decision Records | [docs/adr/](docs/adr/) |
| Runbooks operacionais | [docs/runbooks/](docs/runbooks/) |
| Playbooks técnicos | [docs/playbooks/](docs/playbooks/) |
| Especificações de features | [specs/](specs/) |
