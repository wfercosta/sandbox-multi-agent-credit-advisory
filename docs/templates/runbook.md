---
titulo: <!-- título descritivo do procedimento -->
servico: <!-- nome do serviço ou componente afetado -->
severidade: P2
ultima-revisao: AAAA-MM-DD
---

# Runbook: <!-- título do procedimento -->

## Visão geral

<!-- Descreva em 2-3 frases o que este runbook cobre.
     Inclua quando deve ser executado e quem é o público-alvo
     (ex: plantão de engenharia, time de infra, DBA). -->

## Pré-requisitos

<!-- Liste acessos, ferramentas e conhecimentos necessários antes de iniciar.
     Inclua versões mínimas de ferramentas quando relevante. -->

- Acesso a:
- Ferramentas instaladas:
- Permissões necessárias:

## Procedimento

<!-- Numere cada passo de forma que outro engenheiro possa executar sem contexto adicional.
     Inclua os comandos exatos. Destaque com ATENÇÃO qualquer passo destrutivo ou irreversível. -->

1.

2.

3.

## Verificação

<!-- Descreva como confirmar que o procedimento foi executado com sucesso.
     Inclua comandos de verificação e o output esperado quando possível. -->

```bash
# comando de verificação
```

<!-- Saída esperada: -->

## Rollback

<!-- Descreva como reverter as alterações caso o procedimento falhe ou cause impacto inesperado.
     Se não houver rollback possível, documente isso explicitamente e indique o caminho alternativo. -->

1.

2.

## Troubleshooting

<!-- Preencha com sintomas conhecidos encontrados durante execuções anteriores.
     A coluna "Ação" deve ser prescritiva: diga o que fazer, não apenas o que investigar. -->

| Sintoma | Causa provável | Ação |
|---|---|---|
|  |  |  |

## Referências

<!-- Links para documentação, ADRs, dashboards ou outros runbooks relacionados. -->

-
