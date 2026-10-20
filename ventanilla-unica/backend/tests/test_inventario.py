from datetime import date

import pytest

from ventanilla.inventario import Almacen, Cuenta, Elemento, ErrorInventario, TipoBien, sugerir_tipo

HOY = date(2026, 10, 20)


@pytest.fixture
def almacen() -> Almacen:
    a = Almacen()
    a.registrar_elemento(Elemento("PAP-01", "Resma de papel carta", TipoBien.CONSUMO, "resma"))
    a.registrar_elemento(Elemento("COM-01", "Computador de escritorio", TipoBien.DEVOLUTIVO, vida_util_meses=60))
    return a


def test_consumo_entra_como_inventario_y_sale_como_gasto(almacen):
    almacen.entrada(HOY, "PAP-01", 10, 20_000, "Factura 123")
    almacen.entrada(HOY, "PAP-01", 10, 22_000, "Factura 124")  # promedio = 21.000
    gasto = almacen.salida_consumo(HOY, "PAP-01", 4, "Secretaría de Hacienda")
    assert gasto == 84_000
    assert almacen.existencias["PAP-01"] == 16
    assert almacen.asientos[0].debito == Cuenta.INVENTARIO
    assert almacen.asientos[-1].debito == Cuenta.GASTO_CONSUMO
    assert almacen.gasto_por_dependencia(HOY, HOY) == {"Secretaría de Hacienda": 84_000}


def test_devolutivo_queda_como_activo_con_responsable(almacen):
    almacen.entrada(HOY, "COM-01", 2, 3_000_000, "Contrato CO-2026-010")
    activo = almacen.asignar_activo(HOY, "COM-01", "AL-0001", "Secretaría de Planeación", "Funcionario 1 — Planeación")
    assert activo.costo == 3_000_000
    assert almacen.asientos[-1].debito == Cuenta.ACTIVO_EN_SERVICIO
    assert almacen.gasto_por_dependencia(HOY, HOY) == {}  # entregar un activo no es gasto
    assert almacen.activos_por_dependencia()["Secretaría de Planeación"]["cantidad"] == 1


def test_depreciacion_lineal_y_baja(almacen):
    almacen.entrada(HOY, "COM-01", 1, 6_000_000, "Contrato")
    almacen.asignar_activo(HOY, "COM-01", "AL-0002", "Secretaría de Gobierno", "Jefe — Gobierno")
    assert almacen.depreciar_mes(date(2026, 10, 31)) == 100_000  # 6.000.000 / 60 meses
    almacen.dar_de_baja(date(2026, 11, 5), "AL-0002", "Acta de baja 01")
    assert almacen.asientos[-1].debito == Cuenta.GASTO_BAJA
    assert almacen.asientos[-1].valor == 5_900_000
    assert almacen.activos_por_dependencia() == {}


def test_traslado_cambia_responsable_sin_asiento(almacen):
    almacen.entrada(HOY, "COM-01", 1, 3_000_000, "Contrato")
    almacen.asignar_activo(HOY, "COM-01", "AL-0003", "Secretaría de Hacienda", "Funcionario 1 — Hacienda")
    asientos = len(almacen.asientos)
    almacen.trasladar_activo("AL-0003", "Secretaría de Gobierno", "Funcionario 2 — Gobierno")
    assert len(almacen.asientos) == asientos
    assert almacen.activos["AL-0003"].responsable == "Funcionario 2 — Gobierno"


def test_errores(almacen):
    with pytest.raises(ErrorInventario):
        almacen.salida_consumo(HOY, "PAP-01", 1, "Hacienda")  # sin existencias
    with pytest.raises(ErrorInventario):
        almacen.salida_consumo(HOY, "COM-01", 1, "Hacienda")  # devolutivo no sale como consumo
    with pytest.raises(ErrorInventario):
        almacen.registrar_elemento(Elemento("SIL-01", "Silla", TipoBien.DEVOLUTIVO))  # sin vida útil


def test_sugerir_tipo():
    assert sugerir_tipo(3_000_000, 60, umbral_activo=500_000) == TipoBien.DEVOLUTIVO
    assert sugerir_tipo(20_000, 1, umbral_activo=500_000) == TipoBien.CONSUMO
    assert sugerir_tipo(300_000, 36, umbral_activo=500_000) == TipoBien.CONSUMO  # bajo el umbral
