# sandbox-multi-agent-credit-advisory

## O que é este projeto
Este é um projeto no modelo de monorepo para criação de uma aplicação multi-agente para ajudar os Product Managers, Tech Leads e Engenheiros de Frontend e Engeneheiros de Backend desde o processo de descoberta (product discovery) até a definição da solução técnica, gerando artefatos como, produt requirement document ou one-pager, backlog refinado, com definição de épicos, features e user stories, desenho de solução novos ou evoluções do desenho de solução e refinamentos técnicos, produzindo o Software Design Document para cada história.


## Domínio: Crédito Imobiliário Brasileiro

Todo o sistema gira em torno deste domínio. Não é cenário decorativo — é expertise real.

**Escopo do domínio:**
- Modalidades: SFH, SFI, MCMV/Casa Verde e Amarela, crédito direto com construtora
- Sistemas de amortização: SAC, Price, SAM
- Instrumentos e garantias: alienação fiduciária (Lei 9.514/97), hipoteca, LCI/LIG, CRI
- Regulação: BACEN, CMN, Caixa, ABECIP, Lei 9.514/97, Lei 10.931/04, CDC, LGPD

**Regras críticas para todos os agentes:**
- Afirmações regulatórias exigem citação rastreável ao corpus (lei, artigo, parágrafo, data de vigência)
- O sistema **informa**, nunca **aconselha individualmente** — não somos consultores registrados
- Alucinação regulatória é o erro mais grave: "Lei X diz Y" errado induz decisão errada
- Dados pessoais (CPF, renda) não são retidos sem base legal — LGPD se aplica ao fluxo inteiro

## Stack

* Python 3.13
* uv (gerenciador de pacotes e workspaces)
* LangChain, LangGraph
* Claude API — modelos Anthropic exclusivamente (Opus, Sonnet, Haiku)
* Postgres 17 + pgvector
* Datadog Agent 7
* Terraform
* Kubernetes

## Estrutura do repositório

Abaixo segue uma definição dos principais diretórios do projeto

```
.
├── apps # Diretório onde serão criados as aplicações que serão implantadas nos ambientes como orquestradores ou extensões
├── docs # Diretório onde serão criados os documentos, diagramas, playbooks, templates e decisões de design e arquitetura
├── infra # Diretório onde serão criados scripts de infraestrutura como scripts de IaC, manifestos de kubernetes e outros
├── packages # Diretório onde serão criados  componentes compartilhados e reutilizáveis
│   ├── agents #Diretório para construção de agentes
│   ├── mcp-servers # Diretório para construção de MCP Servers para consumo dos agentes
│   ├── memory # Diretório para construção de componente para integrações com armazenamento e busca de memórias pelos agentes
│   ├── models # Diretŕoio para construção de interações com modelos
│   ├── observability #Diretório para construção de componentes de suporte a observabilidade
│   ├── rag # Diretório para construção de componentes de suporte a RAG
│   ├── shared # Diretório para construção de componentes e configurações compartilhadas
│   └── tools # Diretório para construção de ferramentas em geral par auso do projeto
└── specs # Diretório para armazenamento ds especificações

```

## Comandos do dia a dia

**Lint e formatação**
```
uv run ruff check . # Lint diretório corrente
uv run ruff check --fix # Lint diretório corrente e realiza correções
uv run ruff format /path/to/code/ # Formata aquivos em diretório específico
```

**Executção de testes**
```
uv run pytest # Executa a suite de testes completa
uv run pytest /path/to/file # Executa uma suite de testes em específico
uv run coverage run -m pytest # Executa a suite de testes com coverage
uv run coverage report # Executa a geração do report de testes
```

**Verificações de tipos estáticos**
```
uv run pyright packages/shared   # verifica pacote específico
uv run pyright                   # verifica todo o projeto
```

**Execução de infra local**
Para executar o ambiente a infra para testes locais neste projeto, a partir do diretório ./infra/docker, você pode executar os seguintes comandos:
```
podman-compose -f compose.yaml --env-file ../../.env up -d # Irá subir em modo deatch os containers utilizados neste projeto
podman-compose -f compose.yaml down # Irá parar os containers
```

## Convenções

**Tooling**
* ruff, para lint e formatação dos códigos fontes;
* pyright, para verificação dos tipos estáticos do python;
* pytest, para execução dos testes do projeto;
* podman, para execução dos ambientes de testes locais usando containers;
* podman-compose, para execução de uma composição e containers pré-configurados;

**Convenção de branches**
* main, branch principal do projeto, nunca deve receber commits diretamente. Sempre através de Pull Request/ Merge Requests;
* feature/*, branch utilizada para construção de novas funcionalidades, envio de correções, tarefas de configuração e manutenção;

**Convenções de commits**

Os commits sempre irão seguir este modelo de estrutura:
```
<type>[optional scope]: <description>

[optional body]
```

Os tipos (types) suportados são:
* feat: Nova funcionalidade para o usuário.
* fix: Correção de defeitos para o usuário.
* docs: Mudanças somente em documentação.
* style: Mudanças que não afetam o significado do codigo (white-space, formatting, etc.).
* refactor: Uma mudança de código que não corrige um defeito e nem adiciona uma funcionalidade.
* perf: Uma mudança de código que melhora a performance.
* test: Adiciona testes que estavam faltando ou corrige um existente.
* build: Mudanças que afetam somente o sistema de build ou dependências externas (e.g., npm, make).
* ci: Mudanças nos arquivos e scripts do CI (integração contínua).
* chore: Outras modificações que não afetam arquivos em src ou test (e.g., .gitignore).


**Convenções para geração documentos**

* Specs: toda feature começa com a crição de uma especificação no diretŕoio ```specs``, com o seguinte padrão: specs/NNNN-slug/spec.md
* Diagram: todoa evolução do projeto deve ser a criação ou atualização da visão de arquitetura e design usando um modelo mermaid first e deve ser armazenado no diretório: docs/diagrams/;
* ADRs: toda decisção importante do projeto deve ser gerado uma ADR no diretório docs/adr/ no formato MADR;
* Playbooks: Toda definição de procedimentos, melhores práticas e estratégias padronizadas para execução de tarefas técnias devem ser colocados em: docs/playbooks, usando um formato markdown
* Runbooks: Toda definição de procedimentos operacionais devem ser colocados em: docs/runbooks, usando um formato markdown
* Templates: Toda definição templates padronizados devem ser colocados em: docs/templates, usando um formato markdown

## Agentes do sistema

* **packages/agents/pm/**, Agente especializado em crédito imobiliário responsável por realizar o discovery de necessidades de negócio com base em sua base de conhecimento sobre regulações e informações atuais do produto (KB, knowledge base) e com base em artefatos adicionais como transcições de reuniões e documentos adicionais (KS, Knowledge Sources), além das interações com outros agentes. O use objetivo é gerar PRD (Product Requirement Documents), One-Pager, Backlog bem definido de épicos, features e histórias para consumo dos outros agentes;
* **packages/agents/tech_lead/**, Engenheiro senior, que atua como tech lead de engenheiros de backend e frontend. Ele é responsável, com base no backlog, realizar refinamentos técnico de componentes existentes ou criar novos componentes para solução. O seu refinamento técnico é realizado com apoio de engenheiros especialistas em frontend e backend. Também é reponsável por criar e manter desenhos de solução além de gerar o Software Design Document;
* **packages/agents/backend/**, Engenheiro senior especialista em desenvolvimento backend. Tem conhecimento profundo em Kotlin, Spring boot, Banco de dados relacionais e NoSQL e infraestrutura tanto AWS quanto Kubernetes;
* **packages/agents/frontend/**, Engenheiro senior especialista em desenvolvimento frontend. Tem conhecimento profundo em TypeScript, ReactJS/NextJS e infraestrutura tanto AWS quanto Kubernetes.

## O que nunca fazer
* Criar arquivos fora da estrutura estabelecida do projeto;
* Ignorar schemas definidos do Pydantic;
* Realizar commit diretamente branch main;
* Usar modelos que não sejam Anthropic/Claude;
* Realizar incremento de software sem realizar a devida cobertura de testes;
* Realizar commits sem executar testes locais;
* Realizar commits sem garantir que todos os testes estão executando com sucesso;
* Realizar a immplementação de um plano de implementação de uma spec sem pedir a revisão do usuário antes;
