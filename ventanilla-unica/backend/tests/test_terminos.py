from datetime import date

from ventanilla.modelos import TipoPQRS
from ventanilla.terminos import calcular_fechas, dias_habiles_entre, es_habil, sumar_dias_habiles


def test_festivos_y_fines_de_semana_no_son_habiles():
    assert not es_habil(date(2026, 10, 12))  # Día de la Raza
    assert not es_habil(date(2026, 11, 2))  # Todos los Santos (trasladado)
    assert not es_habil(date(2026, 10, 17))  # sábado
    assert es_habil(date(2026, 10, 13))


def test_conteo_empieza_el_dia_habil_siguiente():
    # Radicada el viernes 9 de octubre; el lunes 12 es festivo → día 1 = martes 13.
    assert sumar_dias_habiles(date(2026, 10, 9), 1) == date(2026, 10, 13)


def test_peticion_general_15_dias_con_festivos():
    vencimiento, interna = calcular_fechas(TipoPQRS.PETICION_GENERAL, date(2026, 10, 9))
    # 13–16 oct (4), 19–23 (9), 26–30 (14), 2 nov festivo → 3 nov (15)
    assert vencimiento == date(2026, 11, 3)
    assert interna == date(2026, 10, 26)  # día hábil 10


def test_terminos_por_tipo():
    radicacion = date(2026, 10, 20)
    for tipo, dias in [(TipoPQRS.DOCUMENTOS, 10), (TipoPQRS.CONSULTA, 30), (TipoPQRS.QUEJA, 15)]:
        vencimiento, interna = calcular_fechas(tipo, radicacion)
        assert dias_habiles_entre(radicacion, vencimiento) == dias
        assert dias_habiles_entre(radicacion, interna) == round(dias * 2 / 3)


def test_dias_habiles_entre_negativo_si_ya_paso():
    assert dias_habiles_entre(date(2026, 10, 20), date(2026, 10, 16)) == -2
