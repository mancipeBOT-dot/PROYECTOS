"""Catálogo de dependencias y funcionarios de la alcaldía."""

import json
from pathlib import Path

from .modelos import Dependencia, Funcionario

DATOS = Path(__file__).resolve().parent.parent / "datos"


class Catalogo:
    def __init__(self, dependencias: list[Dependencia], funcionarios: list[Funcionario]):
        self.dependencias = dependencias
        self.funcionarios = funcionarios

    @classmethod
    def desde_archivo(cls, ruta: Path = DATOS / "alcaldia.json") -> "Catalogo":
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        return cls(
            [Dependencia(**d) for d in datos["dependencias"]],
            [Funcionario(**f) for f in datos["funcionarios"]],
        )

    def nombres_dependencias(self) -> list[str]:
        return [d.nombre for d in self.dependencias]

    def funcionarios_de(self, dependencia: str) -> list[Funcionario]:
        return [f for f in self.funcionarios if f.dependencia == dependencia and f.activo]

    def funcionario(self, funcionario_id: str) -> Funcionario | None:
        return next((f for f in self.funcionarios if f.id == funcionario_id), None)
