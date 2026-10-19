"""Asignación a funcionarios, plan diario por jornada, alertas y escalamiento."""

from collections import defaultdict
from datetime import date, timedelta

from .catalogo import Catalogo
from .modelos import PQRS, Funcionario
from .terminos import DIAS_ALERTA_ROJA, dias_habiles_entre, es_habil, sumar_dias_habiles
from .texto import contiene, normalizar

BLOQUES = ("manana", "tarde")  # 8:00–12:00 y 14:00–18:00


def elegir_funcionario(
    catalogo: Catalogo, dependencia: str, texto: str, carga: dict[str, int]
) -> Funcionario | None:
    """Funcionario de la dependencia que maneja el tema; si hay empate, el de menor carga."""
    candidatos = catalogo.funcionarios_de(dependencia)
    if not candidatos:
        return None
    norm = normalizar(texto)

    def criterio(f: Funcionario):
        maneja_tema = any(contiene(norm, t) for t in f.temas)
        return (not maneja_tema, carga.get(f.id, 0), f.id)

    return min(candidatos, key=criterio)


def _primer_dia_habil(desde: date) -> date:
    return desde if es_habil(desde) else sumar_dias_habiles(desde, 1)


def plan_diario(pqrs: list[PQRS], hoy: date) -> dict[date, dict[str, list[str]]]:
    """Reparte las PQRS abiertas de un funcionario entre los días hábiles hasta su fecha interna.

    Cada PQRS va al bloque (mañana o tarde) con menos carga, lo más temprano posible.
    Las que ya pasaron su fecha interna quedan para hoy.
    """
    inicio = _primer_dia_habil(hoy)
    plan: dict[date, dict[str, list[str]]] = defaultdict(lambda: {b: [] for b in BLOQUES})
    for p in sorted(pqrs, key=lambda p: (p.fecha_interna, p.vencimiento_legal, p.radicado)):
        limite = max(p.fecha_interna, inicio)
        dias, dia = [], inicio
        while dia <= limite:
            if es_habil(dia):
                dias.append(dia)
            dia += timedelta(days=1)
        espacios = [(d, b) for d in dias for b in BLOQUES]
        d, b = min(espacios, key=lambda e: (len(plan[e[0]][e[1]]), e[0], BLOQUES.index(e[1])))
        plan[d][b].append(p.radicado)
    return dict(sorted(plan.items()))


def semaforo(p: PQRS, hoy: date) -> str:
    """rojo: vence en 3 días hábiles o menos (o vencida); verde: radicada hoy o ayer; amarillo: el resto."""
    if dias_habiles_entre(hoy, p.vencimiento_legal) <= DIAS_ALERTA_ROJA:
        return "rojo"
    if dias_habiles_entre(p.fecha_radicacion.date(), hoy) <= 1:
        return "verde"
    return "amarillo"


def resumen_alerta(pqrs: list[PQRS], hoy: date, bloque: str) -> dict:
    """Contenido de la alerta en pantalla completa al inicio de cada jornada."""
    plan = plan_diario(pqrs, hoy)
    dia = _primer_dia_habil(hoy)
    radicados = plan.get(dia, {}).get(bloque, [])
    por_radicado = {p.radicado: p for p in pqrs}
    items = [
        {
            "radicado": r,
            "asunto": por_radicado[r].clasificacion.asunto,
            "vence": por_radicado[r].vencimiento_legal.isoformat(),
            "semaforo": semaforo(por_radicado[r], hoy),
        }
        for r in radicados
    ]
    conteo = {c: sum(1 for i in items if i["semaforo"] == c) for c in ("rojo", "amarillo", "verde")}
    jornada = "esta mañana" if bloque == "manana" else "esta tarde"
    mensaje = (
        f"Tiene {len(items)} PQRS para {jornada}: "
        f"{conteo['rojo']} vencen en 3 días hábiles o menos (rojo), "
        f"{conteo['amarillo']} en curso (amarillo), {conteo['verde']} nuevas (verde)."
    )
    return {"fecha": dia.isoformat(), "bloque": bloque, "total": len(items), **conteo, "pqrs": items, "mensaje": mensaje}


def escalamientos(pqrs: list[PQRS], hoy: date) -> list[dict]:
    """A 3 días hábiles del vencimiento → jefe de dependencia. Vencida → Control Interno."""
    resultado = []
    for p in pqrs:
        restantes = dias_habiles_entre(hoy, p.vencimiento_legal)
        if restantes < 0:
            resultado.append({"radicado": p.radicado, "nivel": "control_interno", "dias_restantes": restantes})
        elif restantes <= DIAS_ALERTA_ROJA:
            resultado.append({"radicado": p.radicado, "nivel": "jefe", "dias_restantes": restantes})
    return resultado
