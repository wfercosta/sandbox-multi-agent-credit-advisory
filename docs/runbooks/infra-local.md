---
titulo: Operação da infraestrutura local de desenvolvimento
servico: infra-local
severidade: P3
ultima-revisao: 2026-04-20
---

# Runbook: Operação da infraestrutura local de desenvolvimento

## Visão geral

Este runbook cobre as operações do dia a dia da infraestrutura local de desenvolvimento:
subir, verificar, parar e limpar os containers gerenciados via podman-compose.
O ambiente é composto por Postgres 17 com extensão pgvector e Datadog Agent 7.
Público-alvo: qualquer desenvolvedor do projeto antes de rodar testes ou trabalhar
com agentes localmente.

## Pré-requisitos

- Acesso a: repositório clonado localmente
- Ferramentas instaladas: `podman`, `podman-compose`
- Arquivo `.env` presente na raiz do repositório com as variáveis:
  `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DD_API_KEY`, `DD_SITE`

## Procedimento

### Subir a infraestrutura

1. A partir da raiz do repositório, suba os containers em modo detached:

   ```bash
   cd infra/docker && podman-compose -f compose.yaml --env-file ../../.env up -d
   ```

2. Aguarde o Postgres atingir o estado healthy (o health check executa `pg_isready`
   a cada 10s com até 5 tentativas):

   ```bash
   podman inspect sandbox-multi-agent-credit-advisory_postgres_1 \
     --format '{{.State.Health.Status}}'
   ```

   Aguarde o retorno `healthy` antes de continuar.

3. O Datadog Agent demora aproximadamente 60 segundos para inicializar no Podman.
   Verifique o status com:

   ```bash
   podman inspect sandbox-multi-agent-credit-advisory_datadog-agent_1 \
     --format '{{.State.Status}}'
   ```

   O retorno esperado é `running`. O container não possui health check configurado —
   use o passo de verificação abaixo para confirmar que o agente está operacional.

### Parar a infraestrutura

4. Para parar os containers sem remover os volumes:

   ```bash
   cd infra/docker && podman-compose -f compose.yaml down
   ```

### Limpar volumes

5. **ATENÇÃO — irreversível:** Para remover os containers e o volume `postgres_data`
   (todos os dados do banco serão perdidos):

   ```bash
   cd infra/docker && podman-compose -f compose.yaml down -v
   ```

## Verificação

### Postgres e pgvector

Confirme que o Postgres está aceitando conexões e que a extensão pgvector foi inicializada:

```bash
podman exec sandbox-multi-agent-credit-advisory_postgres_1 \
  psql -U credit_advisory -d credit_advisory \
  -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
```

Saída esperada:

```
 extname | extversion
---------+------------
 vector  | 0.8.x
(1 row)
```

### Datadog Agent

Confirme que o endpoint APM está respondendo:

```bash
curl -s http://localhost:8126/info | python3 -m json.tool | grep version
```

Saída esperada: objeto JSON com campo `version` preenchido.

Confirme que o endpoint DogStatsD está acessível (UDP — apenas verifica que a porta está aberta):

```bash
podman port sandbox-multi-agent-credit-advisory_datadog-agent_1
```

Saída esperada: linhas com `8125/udp -> 0.0.0.0:8125` e `8126/tcp -> 0.0.0.0:8126`.

## Rollback

Este ambiente é efêmero e local — não há rollback de estado de produção envolvido.

1. Se os containers estiverem em estado inconsistente, pare-os:

   ```bash
   cd infra/docker && podman-compose -f compose.yaml down
   ```

2. Remova containers e volumes para partir de um estado limpo:

   ```bash
   cd infra/docker && podman-compose -f compose.yaml down -v
   ```

3. Siga o procedimento de subida novamente a partir do passo 1.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---|---|---|
| `podman-compose up` falha com "port already in use" na 5432 | Outra instância do Postgres rodando localmente | Execute `podman ps` e `ss -tlnp \| grep 5432` para identificar o processo; pare-o antes de subir o compose |
| `pg_isready` retorna `no response` após 50s | Container ainda inicializando ou falha na criação do banco | Verifique logs com `podman logs sandbox-multi-agent-credit-advisory_postgres_1` |
| Extensão `vector` não encontrada no banco | Script de init não foi executado (banco já existia no volume) | Limpe o volume (`down -v`) e suba novamente; o init só roda na criação do banco |
| `curl localhost:8126/info` retorna connection refused após 90s | Datadog Agent falhou na inicialização | Verifique logs com `podman logs sandbox-multi-agent-credit-advisory_datadog-agent_1`; confirme que `DD_API_KEY` está preenchida no `.env` |
| Datadog Agent fica reiniciando em loop | `DD_API_KEY` inválida ou `DD_SITE` incorreto | Corrija os valores no `.env` e execute `down` seguido de `up -d` |

## Referências

- Compose: [`infra/docker/compose.yaml`](../../infra/docker/compose.yaml)
- Script de inicialização do pgvector: [`infra/docker/init/01-extensions.sql`](../../infra/docker/init/01-extensions.sql)
- Documentação pgvector: https://github.com/pgvector/pgvector
- Datadog Agent — configuração por variáveis de ambiente: https://docs.datadoghq.com/agent/configuration/agent-configuration-files/
