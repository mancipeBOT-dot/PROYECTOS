"""Inventarios de Bienes y Servicios: entradas, salidas, gasto y activos.

Regla contable (entidades de gobierno, Contaduría General de la Nación):
- Bien de CONSUMO (papelería, aseo, repuestos): entra al almacén como inventario y,
  cuando sale para una dependencia, se reconoce como GASTO de esa dependencia.
- Bien DEVOLUTIVO (computadores, muebles, vehículos): entra como bien en bodega y,
  cuando se entrega para uso, queda como ACTIVO (propiedad, planta y equipo) a cargo de
  un responsable; se deprecia mes a mes y solo sale con una baja.

Los nombres de cuentas son descriptivos; los códigos del plan de cuentas se toman de Génesis.
Valoración por costo promedio ponderado.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class TipoBien(str, Enum):
    CONSUMO = "consumo"
    DEVOLUTIVO = "devolutivo"


class Cuenta(str, Enum):
    INVENTARIO = "Inventario de materiales y suministros"
    BIENES_EN_BODEGA = "Bienes muebles en bodega"
    ACTIVO_EN_SERVICIO = "Propiedad, planta y equipo en servicio"
    DEPRECIACION_ACUMULADA = "Depreciación acumulada"
    GASTO_CONSUMO = "Gasto de materiales y suministros"
    GASTO_DEPRECIACION = "Gasto de depreciación"
    GASTO_BAJA = "Pérdida por baja de bienes"
    CUENTAS_POR_PAGAR = "Cuentas por pagar"


@dataclass
class Elemento:
    codigo: str
    nombre: str
    tipo: TipoBien
    unidad: str = "unidad"
    vida_util_meses: int = 0  # solo devolutivos


@dataclass
class Asiento:
    fecha: date
    debito: Cuenta
    credito: Cuenta
    valor: float
    dependencia: str = ""
    detalle: str = ""


@dataclass
class ActivoAsignado:
    placa: str
    codigo: str
    dependencia: str
    responsable: str
    costo: float
    fecha_servicio: date
    vida_util_meses: int
    depreciacion_acumulada: float = 0.0
    dado_de_baja: bool = False


class ErrorInventario(Exception):
    pass


def sugerir_tipo(valor_unitario: float, vida_util_meses: int, umbral_activo: float) -> TipoBien:
    """Sugerencia para elementos nuevos: dura más de un año y supera el umbral de la política contable."""
    return TipoBien.DEVOLUTIVO if vida_util_meses > 12 and valor_unitario >= umbral_activo else TipoBien.CONSUMO


@dataclass
class Almacen:
    elementos: dict[str, Elemento] = field(default_factory=dict)
    existencias: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    costo_promedio: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    activos: dict[str, ActivoAsignado] = field(default_factory=dict)
    asientos: list[Asiento] = field(default_factory=list)

    def registrar_elemento(self, elemento: Elemento) -> None:
        if elemento.tipo == TipoBien.DEVOLUTIVO and elemento.vida_util_meses <= 0:
            raise ErrorInventario("Un bien devolutivo necesita vida útil en meses")
        self.elementos[elemento.codigo] = elemento

    def _elemento(self, codigo: str) -> Elemento:
        if codigo not in self.elementos:
            raise ErrorInventario(f"Elemento no registrado: {codigo}")
        return self.elementos[codigo]

    def entrada(self, fecha: date, codigo: str, cantidad: float, valor_unitario: float, soporte: str) -> None:
        """Compra o ingreso al almacén. `soporte`: factura, contrato o acta."""
        e = self._elemento(codigo)
        if cantidad <= 0 or valor_unitario < 0:
            raise ErrorInventario("Cantidad y valor deben ser positivos")
        total_previo = self.existencias[codigo] * self.costo_promedio[codigo]
        self.existencias[codigo] += cantidad
        self.costo_promedio[codigo] = (total_previo + cantidad * valor_unitario) / self.existencias[codigo]
        cuenta = Cuenta.INVENTARIO if e.tipo == TipoBien.CONSUMO else Cuenta.BIENES_EN_BODEGA
        self.asientos.append(Asiento(fecha, cuenta, Cuenta.CUENTAS_POR_PAGAR, cantidad * valor_unitario, detalle=f"Entrada {e.nombre} · {soporte}"))

    def salida_consumo(self, fecha: date, codigo: str, cantidad: float, dependencia: str) -> float:
        """Entrega de bienes de consumo a una dependencia. Devuelve el gasto reconocido."""
        e = self._elemento(codigo)
        if e.tipo != TipoBien.CONSUMO:
            raise ErrorInventario("Los bienes devolutivos se entregan con asignar_activo")
        if cantidad > self.existencias[codigo]:
            raise ErrorInventario(f"Existencias insuficientes de {e.nombre}: hay {self.existencias[codigo]}")
        valor = cantidad * self.costo_promedio[codigo]
        self.existencias[codigo] -= cantidad
        self.asientos.append(Asiento(fecha, Cuenta.GASTO_CONSUMO, Cuenta.INVENTARIO, valor, dependencia, f"Salida {cantidad} {e.unidad} de {e.nombre}"))
        return valor

    def asignar_activo(self, fecha: date, codigo: str, placa: str, dependencia: str, responsable: str) -> ActivoAsignado:
        """Entrega de un bien devolutivo para uso: pasa de bodega a activo en servicio con responsable."""
        e = self._elemento(codigo)
        if e.tipo != TipoBien.DEVOLUTIVO:
            raise ErrorInventario("Los bienes de consumo se entregan con salida_consumo")
        if self.existencias[codigo] < 1:
            raise ErrorInventario(f"No hay {e.nombre} en bodega")
        if placa in self.activos:
            raise ErrorInventario(f"La placa {placa} ya existe")
        costo = self.costo_promedio[codigo]
        self.existencias[codigo] -= 1
        activo = ActivoAsignado(placa, codigo, dependencia, responsable, costo, fecha, e.vida_util_meses)
        self.activos[placa] = activo
        self.asientos.append(Asiento(fecha, Cuenta.ACTIVO_EN_SERVICIO, Cuenta.BIENES_EN_BODEGA, costo, dependencia, f"{e.nombre} placa {placa} a {responsable}"))
        return activo

    def trasladar_activo(self, placa: str, dependencia: str, responsable: str) -> None:
        """Cambio de responsable o dependencia. No genera asiento: el activo sigue siendo de la alcaldía."""
        a = self._activo(placa)
        a.dependencia, a.responsable = dependencia, responsable

    def depreciar_mes(self, fecha: date) -> float:
        """Depreciación lineal mensual de todos los activos en servicio."""
        total = 0.0
        for a in self.activos.values():
            if a.dado_de_baja:
                continue
            cuota = min(a.costo / a.vida_util_meses, a.costo - a.depreciacion_acumulada)
            if cuota <= 0:
                continue
            a.depreciacion_acumulada += cuota
            total += cuota
            self.asientos.append(Asiento(fecha, Cuenta.GASTO_DEPRECIACION, Cuenta.DEPRECIACION_ACUMULADA, cuota, a.dependencia, f"Depreciación placa {a.placa}"))
        return total

    def dar_de_baja(self, fecha: date, placa: str, acta: str) -> None:
        """Retiro del activo (daño, obsolescencia, pérdida). El valor no depreciado es pérdida."""
        a = self._activo(placa)
        pendiente = a.costo - a.depreciacion_acumulada
        if pendiente > 0:
            self.asientos.append(Asiento(fecha, Cuenta.GASTO_BAJA, Cuenta.ACTIVO_EN_SERVICIO, pendiente, a.dependencia, f"Baja placa {placa} · {acta}"))
        a.dado_de_baja = True

    def _activo(self, placa: str) -> ActivoAsignado:
        if placa not in self.activos or self.activos[placa].dado_de_baja:
            raise ErrorInventario(f"Activo no encontrado o dado de baja: {placa}")
        return self.activos[placa]

    # --- Reportes ---

    def gasto_por_dependencia(self, desde: date, hasta: date) -> dict[str, float]:
        gastos = (Cuenta.GASTO_CONSUMO, Cuenta.GASTO_DEPRECIACION, Cuenta.GASTO_BAJA)
        resultado: dict[str, float] = defaultdict(float)
        for a in self.asientos:
            if a.debito in gastos and desde <= a.fecha <= hasta:
                resultado[a.dependencia] += a.valor
        return {k: round(v, 2) for k, v in sorted(resultado.items())}

    def activos_por_dependencia(self) -> dict[str, dict]:
        resultado: dict[str, dict] = defaultdict(lambda: {"cantidad": 0, "costo": 0.0, "valor_en_libros": 0.0})
        for a in self.activos.values():
            if a.dado_de_baja:
                continue
            r = resultado[a.dependencia]
            r["cantidad"] += 1
            r["costo"] += a.costo
            r["valor_en_libros"] += a.costo - a.depreciacion_acumulada
        return {k: {**v, "costo": round(v["costo"], 2), "valor_en_libros": round(v["valor_en_libros"], 2)} for k, v in sorted(resultado.items())}

    def saldo_almacen(self) -> dict[str, dict]:
        return {
            c: {"nombre": self.elementos[c].nombre, "cantidad": q, "valor": round(q * self.costo_promedio[c], 2)}
            for c, q in sorted(self.existencias.items()) if q > 0
        }
