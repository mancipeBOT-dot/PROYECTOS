"""Flujo completo de una PQRS: radicar → clasificar → calcular términos → asignar → cerrar.

El almacenamiento es en memoria para el prototipo; se reemplaza por PostgreSQL en producción.
"""

from collections import Counter
from datetime import date, datetime

from .asignacion import elegir_funcionario, escalamientos, plan_diario, resumen_alerta
from .catalogo import Catalogo
from .clasificador import Clasificador
from .modelos import PQRS, Canal, Estado, TipoPQRS
from .terminos import calcular_fechas, sumar_dias_habiles

UMBRAL_CONFIANZA = 0.80
DIAS_TRASLADO = 5  # Ley 1755 de 2015, art. 21


class ErrorVentanilla(Exception):
    pass


class Ventanilla:
    def __init__(self, catalogo: Catalogo, clasificador: Clasificador):
        self.catalogo = catalogo
        self.clasificador = clasificador
        self.pqrs: dict[str, PQRS] = {}

    def _nuevo_radicado(self, fecha: datetime) -> str:
        return f"VU-{fecha.year}-{len(self.pqrs) + 1:06d}"

    def _carga(self) -> dict[str, int]:
        return Counter(p.funcionario_id for p in self.abiertas() if p.funcionario_id)

    def radicar(self, texto: str, canal: Canal, fecha: datetime | None = None) -> PQRS:
        fecha = fecha or datetime.now()
        clasificacion = self.clasificador.clasificar(texto)

        if not clasificacion.competencia_alcaldia:
            estado = Estado.TRASLADO
            vencimiento = sumar_dias_habiles(fecha.date(), DIAS_TRASLADO)
            interna = sumar_dias_habiles(fecha.date(), 3)
        else:
            vencimiento, interna = calcular_fechas(clasificacion.tipo, fecha.date())
            confiable = clasificacion.confianza >= UMBRAL_CONFIANZA or clasificacion.tipo == TipoPQRS.TUTELA
            estado = Estado.ASIGNADA if confiable else Estado.REVISION

        funcionario = None
        if estado != Estado.REVISION:
            funcionario = elegir_funcionario(self.catalogo, clasificacion.dependencia, texto, self._carga())

        pqrs = PQRS(
            radicado=self._nuevo_radicado(fecha),
            canal=canal,
            fecha_radicacion=fecha,
            texto=texto,
            clasificacion=clasificacion,
            estado=estado,
            funcionario_id=funcionario.id if funcionario else None,
            vencimiento_legal=vencimiento,
            fecha_interna=interna,
        )
        self.pqrs[pqrs.radicado] = pqrs
        return pqrs

    def obtener(self, radicado: str) -> PQRS:
        if radicado not in self.pqrs:
            raise ErrorVentanilla(f"No existe el radicado {radicado}")
        return self.pqrs[radicado]

    def confirmar(self, radicado: str, dependencia: str) -> PQRS:
        """El asignador confirma o corrige la dependencia de una PQRS en revisión."""
        p = self.obtener(radicado)
        if dependencia not in self.catalogo.nombres_dependencias():
            raise ErrorVentanilla(f"Dependencia desconocida: {dependencia}")
        p.clasificacion.dependencia = dependencia
        funcionario = elegir_funcionario(self.catalogo, dependencia, p.texto, self._carga())
        p.funcionario_id = funcionario.id if funcionario else None
        p.estado = Estado.ASIGNADA
        return p

    def cerrar(self, radicado: str, oficio_salida: str, fecha: date | None = None) -> PQRS:
        p = self.obtener(radicado)
        p.estado = Estado.RESPONDIDA
        p.oficio_salida = oficio_salida
        p.fecha_cierre = fecha or date.today()
        return p

    def abiertas(self) -> list[PQRS]:
        return [p for p in self.pqrs.values() if p.estado != Estado.RESPONDIDA]

    def en_revision(self) -> list[PQRS]:
        return [p for p in self.pqrs.values() if p.estado == Estado.REVISION]

    def abiertas_de(self, funcionario_id: str) -> list[PQRS]:
        return [p for p in self.abiertas() if p.funcionario_id == funcionario_id]

    def plan(self, funcionario_id: str, hoy: date) -> dict:
        return plan_diario(self.abiertas_de(funcionario_id), hoy)

    def alerta(self, funcionario_id: str, hoy: date, bloque: str) -> dict:
        return resumen_alerta(self.abiertas_de(funcionario_id), hoy, bloque)

    def escalamientos(self, hoy: date) -> list[dict]:
        return escalamientos(self.abiertas(), hoy)

    def consulta_ciudadano(self, radicado: str) -> dict:
        """Lo único que ve el ciudadano: estado, dependencia y fechas. Sin datos internos."""
        p = self.obtener(radicado)
        return {
            "radicado": p.radicado,
            "estado": p.estado.value,
            "dependencia": p.clasificacion.dependencia if p.estado != Estado.REVISION else "En asignación",
            "fecha_radicacion": p.fecha_radicacion.date().isoformat(),
            "vencimiento": p.vencimiento_legal.isoformat(),
        }
