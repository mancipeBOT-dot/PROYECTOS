from datetime import date, datetime

from fastapi.testclient import TestClient

from ventanilla.api import crear_app
from ventanilla.modelos import Canal, Estado

LUNES = datetime(2026, 10, 19, 9, 0)


def test_radicar_asigna_funcionario_del_tema(ventanilla):
    p = ventanilla.radicar("Solicito licencia de construcción para mi casa, adjunto el plano", Canal.PRESENCIAL, LUNES)
    assert p.estado == Estado.ASIGNADA
    assert p.funcionario_id == "PL-1"  # maneja licencias de construcción
    assert p.radicado == "VU-2026-000001"


def test_reparte_por_carga_cuando_nadie_maneja_el_tema(ventanilla):
    ids = {
        ventanilla.radicar("Solicito audiencia con el alcalde y revisar el plan de desarrollo", Canal.WEB, LUNES).funcionario_id,
        ventanilla.radicar("Rendición de cuentas del alcalde", Canal.WEB, LUNES).funcionario_id,
    }
    assert len(ids) == 2


def test_baja_confianza_queda_en_revision_y_se_confirma(ventanilla):
    p = ventanilla.radicar("Solicito que revisen la vía", Canal.WEB, LUNES)
    assert p.estado == Estado.REVISION and p.funcionario_id is None
    ventanilla.confirmar(p.radicado, "Secretaría de Obras Públicas")
    assert p.estado == Estado.ASIGNADA and p.funcionario_id.startswith("OP-")


def test_plan_diario_no_pasa_la_fecha_interna(ventanilla):
    for _ in range(6):
        ventanilla.radicar("Paz y salvo del impuesto predial", Canal.CORREO, LUNES)
    plan = ventanilla.plan("HA-1", date(2026, 10, 19))
    internas = {p.radicado: p.fecha_interna for p in ventanilla.abiertas_de("HA-1")}
    for dia, bloques in plan.items():
        for radicados in bloques.values():
            assert all(dia <= internas[r] for r in radicados)
    asignadas = [r for bloques in plan.values() for rs in bloques.values() for r in rs]
    assert sorted(asignadas) == sorted(internas)


def test_alerta_y_escalamiento(ventanilla):
    p = ventanilla.radicar("Paz y salvo del impuesto predial", Canal.CORREO, LUNES)
    alerta = ventanilla.alerta(p.funcionario_id, date(2026, 10, 19), "manana")
    assert alerta["total"] == 1 and alerta["verde"] == 1
    # Documentos: 10 días hábiles → vence el 3 de noviembre. El 29 de octubre faltan 3.
    assert [e["nivel"] for e in ventanilla.escalamientos(date(2026, 10, 29))] == ["jefe"]
    assert [e["nivel"] for e in ventanilla.escalamientos(date(2026, 11, 4))] == ["control_interno"]


def test_cerrar_saca_de_abiertas(ventanilla):
    p = ventanilla.radicar("Paz y salvo del impuesto predial", Canal.CORREO, LUNES)
    ventanilla.cerrar(p.radicado, "OF-2026-100")
    assert ventanilla.abiertas() == []


def test_api_radicar_y_consulta_ciudadano(ventanilla):
    cliente = TestClient(crear_app(ventanilla))
    r = cliente.post("/pqrs", json={"texto": "Factura del acueducto muy alta, revisar medidor", "canal": "web"})
    assert r.status_code == 200
    radicado = r.json()["radicado"]
    consulta = cliente.get(f"/consulta/{radicado}").json()
    assert consulta["dependencia"] == "Unidad de Servicios Públicos"
    assert "texto" not in consulta  # el ciudadano no ve datos internos
    assert cliente.get("/consulta/VU-2026-999999").status_code == 404
    assert cliente.get("/funcionarios/SP-1/alerta", params={"bloque": "tarde"}).status_code == 200
