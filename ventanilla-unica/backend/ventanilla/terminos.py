"""Términos legales de respuesta (Ley 1755 de 2015, art. 14) en días hábiles de Colombia."""

from datetime import date, timedelta
from functools import lru_cache

import holidays

from .modelos import TipoPQRS

TERMINO_DIAS_HABILES = {
    TipoPQRS.PETICION_GENERAL: 15,
    TipoPQRS.QUEJA: 15,
    TipoPQRS.RECLAMO: 15,
    TipoPQRS.DENUNCIA: 15,
    TipoPQRS.DOCUMENTOS: 10,
    TipoPQRS.ENTRE_AUTORIDADES: 10,
    TipoPQRS.CONSULTA: 30,
    # La tutela trae su propio plazo en el auto del juez; 2 días hábiles es el mínimo
    # habitual y obliga a que Jurídica revise el plazo real el mismo día.
    TipoPQRS.TUTELA: 2,
}

DIAS_ALERTA_ROJA = 3  # días hábiles antes del vencimiento legal


@lru_cache(maxsize=16)
def _festivos(anio: int) -> holidays.HolidayBase:
    return holidays.Colombia(years=anio)


def es_habil(dia: date) -> bool:
    return dia.weekday() < 5 and dia not in _festivos(dia.year)


def sumar_dias_habiles(desde: date, dias: int) -> date:
    """Día hábil número `dias` contado a partir del día siguiente a `desde`."""
    actual = desde
    contados = 0
    while contados < dias:
        actual += timedelta(days=1)
        if es_habil(actual):
            contados += 1
    return actual


def dias_habiles_entre(desde: date, hasta: date) -> int:
    """Días hábiles en (desde, hasta]. Negativo si `hasta` es anterior a `desde`."""
    if hasta < desde:
        return -dias_habiles_entre(hasta, desde)
    return sum(1 for i in range(1, (hasta - desde).days + 1) if es_habil(desde + timedelta(days=i)))


def calcular_fechas(tipo: TipoPQRS, radicacion: date) -> tuple[date, date]:
    """Devuelve (vencimiento legal, fecha interna).

    La fecha interna es a los dos tercios del término (día 10 de 15) para dejar
    tiempo de revisión y firma.
    """
    termino = TERMINO_DIAS_HABILES[tipo]
    vencimiento = sumar_dias_habiles(radicacion, termino)
    interna = sumar_dias_habiles(radicacion, max(1, round(termino * 2 / 3)))
    return vencimiento, interna
