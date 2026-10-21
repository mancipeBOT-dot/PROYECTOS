"""Modelos de datos del sistema."""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class TipoPQRS(str, Enum):
    PETICION_GENERAL = "peticion_general"
    DOCUMENTOS = "documentos"
    CONSULTA = "consulta"
    QUEJA = "queja"
    RECLAMO = "reclamo"
    DENUNCIA = "denuncia"
    ENTRE_AUTORIDADES = "entre_autoridades"
    TUTELA = "tutela"


class Canal(str, Enum):
    CORREO = "correo"
    PRESENCIAL = "presencial"
    WEB = "web"
    REDES = "redes"


class Estado(str, Enum):
    REVISION = "revision"  # la IA no está segura; el asignador debe confirmar
    ASIGNADA = "asignada"
    RESPONDIDA = "respondida"
    TRASLADO = "traslado"  # no es competencia de la alcaldía


class Peticionario(BaseModel):
    nombre: str = ""
    documento: str = ""
    correo_respuesta: str = ""
    direccion: str = ""


class Clasificacion(BaseModel):
    tipo: TipoPQRS
    dependencia: str
    prioritario: bool = False
    motivo_prioridad: str = ""
    competencia_alcaldia: bool = True
    asunto: str
    peticionario: Peticionario = Field(default_factory=Peticionario)
    confianza: float = Field(ge=0, le=1)
    metodo: str = "palabras_clave"  # "ia" o "palabras_clave"


class Dependencia(BaseModel):
    nombre: str
    palabras_clave: list[str]


class Funcionario(BaseModel):
    id: str
    nombre: str
    dependencia: str
    correo: str
    temas: list[str] = []
    activo: bool = True
    es_jefe: bool = False  # el jefe aprueba asignaciones; no recibe PQRS automáticamente
    planta: bool = True  # solo al personal de planta se le mide horario y actividad


class PQRS(BaseModel):
    radicado: str
    canal: Canal
    fecha_radicacion: datetime
    texto: str
    archivo_original: str = ""  # ruta del PDF o imagen original (prueba documental)
    clasificacion: Clasificacion
    estado: Estado
    funcionario_id: str | None = None
    vencimiento_legal: date
    fecha_interna: date
    aprobada_por_jefe: bool = False
    dependencias_devueltas: list[str] = []  # dependencias que dijeron "no es de mi competencia"
    oficio_salida: str = ""
    fecha_cierre: date | None = None
