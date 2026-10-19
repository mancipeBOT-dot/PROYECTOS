"""API web del sistema. Ejecutar: uvicorn ventanilla.api:app --reload"""

import os
from datetime import date, datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .catalogo import Catalogo
from .clasificador import Clasificador, ClasificadorIA
from .modelos import PQRS, Canal
from .servicio import ErrorVentanilla, Ventanilla


class NuevaPQRS(BaseModel):
    texto: str
    canal: Canal
    fecha_radicacion: datetime | None = None


class Confirmacion(BaseModel):
    dependencia: str


class Cierre(BaseModel):
    oficio_salida: str


def crear_ventanilla() -> Ventanilla:
    catalogo = Catalogo.desde_archivo()
    # La IA se activa con VUI_USAR_IA=1 y credenciales de la API de Claude.
    ia = ClasificadorIA(catalogo) if os.getenv("VUI_USAR_IA") == "1" else None
    return Ventanilla(catalogo, Clasificador(catalogo, ia))


def crear_app(ventanilla: Ventanilla | None = None) -> FastAPI:
    vu = ventanilla or crear_ventanilla()
    app = FastAPI(title="Ventanilla Única Inteligente — Software JRLM", version="0.1.0")

    def buscar(radicado: str) -> PQRS:
        try:
            return vu.obtener(radicado)
        except ErrorVentanilla as error:
            raise HTTPException(404, str(error))

    @app.post("/pqrs", response_model=PQRS)
    def radicar(datos: NuevaPQRS):
        return vu.radicar(datos.texto, datos.canal, datos.fecha_radicacion)

    @app.get("/pqrs", response_model=list[PQRS])
    def listar(estado: str | None = None):
        return [p for p in vu.pqrs.values() if estado is None or p.estado.value == estado]

    @app.get("/pqrs/{radicado}", response_model=PQRS)
    def ver(radicado: str):
        return buscar(radicado)

    @app.post("/pqrs/{radicado}/confirmar", response_model=PQRS)
    def confirmar(radicado: str, datos: Confirmacion):
        buscar(radicado)
        try:
            return vu.confirmar(radicado, datos.dependencia)
        except ErrorVentanilla as error:
            raise HTTPException(422, str(error))

    @app.post("/pqrs/{radicado}/cerrar", response_model=PQRS)
    def cerrar(radicado: str, datos: Cierre):
        buscar(radicado)
        return vu.cerrar(radicado, datos.oficio_salida)

    @app.get("/funcionarios/{funcionario_id}/alerta")
    def alerta(funcionario_id: str, bloque: str = Query("manana", pattern="^(manana|tarde)$"), fecha: date | None = None):
        if vu.catalogo.funcionario(funcionario_id) is None:
            raise HTTPException(404, "Funcionario no encontrado")
        return vu.alerta(funcionario_id, fecha or date.today(), bloque)

    @app.get("/funcionarios/{funcionario_id}/plan")
    def plan(funcionario_id: str, fecha: date | None = None):
        if vu.catalogo.funcionario(funcionario_id) is None:
            raise HTTPException(404, "Funcionario no encontrado")
        return {d.isoformat(): bloques for d, bloques in vu.plan(funcionario_id, fecha or date.today()).items()}

    @app.get("/escalamientos")
    def escalar(fecha: date | None = None):
        return vu.escalamientos(fecha or date.today())

    @app.get("/consulta/{radicado}")
    def consulta(radicado: str):
        buscar(radicado)
        return vu.consulta_ciudadano(radicado)

    return app


app = crear_app()
