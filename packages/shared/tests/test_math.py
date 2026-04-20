from decimal import Decimal

import pytest

from shared.math import calcular_amortizacao_sac


def test_numero_de_parcelas_igual_ao_prazo() -> None:
    parcelas = calcular_amortizacao_sac(
        valor_financiado=Decimal("100000"),
        prazo_meses=360,
        taxa_mensal=Decimal("0.008"),
    )
    assert len(parcelas) == 360


def test_primeira_parcela_maior_que_ultima() -> None:
    """No SAC a parcela decresce ao longo do tempo."""
    parcelas = calcular_amortizacao_sac(
        valor_financiado=Decimal("100000"),
        prazo_meses=360,
        taxa_mensal=Decimal("0.008"),
    )
    assert parcelas[0] > parcelas[-1]


def test_parcelas_decrescentes() -> None:
    """Cada parcela deve ser menor ou igual à anterior"""
    parcelas = calcular_amortizacao_sac(
        valor_financiado=Decimal("100000"),
        prazo_meses=360,
        taxa_mensal=Decimal("0.008"),
    )
    assert all(parcelas[i] >= parcelas[i + 1] for i in range(len(parcelas) - 1))


def test_prazo_invalido_levanta_erro() -> None:
    with pytest.raises(ValueError, match="prazo_meses deve ser maior que zero"):
        calcular_amortizacao_sac(
            valor_financiado=Decimal("100000"),
            prazo_meses=0,
            taxa_mensal=Decimal("0.008"),
        )
