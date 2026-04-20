from decimal import Decimal


def calcular_amortizacao_sac(
    valor_financiado: Decimal, prazo_meses: int, taxa_mensal: Decimal
) -> list[Decimal]:
    """
    No SAC a amortização é constante. A parcela decresce porque
    os juros incidem sobre o saldo devedor que diminui a cada mês.

    Args:
        valor_financiamento: Valor total do financiamento em Reais.
        prazo_meses: Número de meses do financiamento.
        taxa_mensal: Taxa de juros mensal em decimal (ex: 0.008 para 0,8%)

    Returns:
        Lista com os valor de cada parcela, do primeiro ao último mês
    """

    if prazo_meses <= 0:
        raise ValueError("prazo_meses deve ser maior que zero")

    amortizacao = valor_financiado / Decimal(prazo_meses)
    parcelas = []
    saldo_devedor = valor_financiado

    for _ in range(prazo_meses):
        juros = saldo_devedor * taxa_mensal
        parcela = amortizacao + juros
        parcelas.append(parcela.quantize(Decimal("0.01")))
        saldo_devedor -= amortizacao

    return parcelas
