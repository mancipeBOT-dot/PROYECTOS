import json
from types import SimpleNamespace

import anthropic
import httpx

from ventanilla.catalogo import DATOS
from ventanilla.clasificador import Clasificador, ClasificadorIA, ClasificadorPalabrasClave
from ventanilla.modelos import TipoPQRS


def test_palabras_clave_sobre_casos_de_prueba(catalogo):
    clasificador = ClasificadorPalabrasClave(catalogo)
    casos = json.loads((DATOS / "pqrs_prueba.json").read_text(encoding="utf-8"))
    correctos = sum(clasificador.clasificar(c["texto"]).dependencia == c["dependencia_esperada"] for c in casos)
    assert correctos / len(casos) >= 0.9


def test_extrae_correo_y_cedula(catalogo):
    c = ClasificadorPalabrasClave(catalogo).clasificar(
        "Solicito paz y salvo del predial. C.C. 1.234.567. Respuesta a pedro@correo.ejemplo"
    )
    assert c.peticionario.correo_respuesta == "pedro@correo.ejemplo"
    assert c.peticionario.documento == "1234567"
    assert c.tipo == TipoPQRS.DOCUMENTOS


def test_tutela_va_a_juridica(catalogo):
    c = ClasificadorPalabrasClave(catalogo).clasificar("Se notifica acción de tutela por el predial")
    assert c.tipo == TipoPQRS.TUTELA
    assert c.dependencia == "Oficina Jurídica"


def test_sin_competencia_marca_traslado(catalogo):
    c = ClasificadorPalabrasClave(catalogo).clasificar("La EPS no me entrega los medicamentos")
    assert not c.competencia_alcaldia
    assert c.dependencia == "Oficina Jurídica"


def test_prioridad_menor_de_edad(catalogo):
    c = ClasificadorPalabrasClave(catalogo).clasificar("Mi hijo es menor de edad y necesita el subsidio")
    assert c.prioritario
    assert c.motivo_prioridad == "menor de edad"


class _ClienteFalso:
    """Imita client.beta.messages.create sin llamar a la API."""

    def __init__(self, respuesta=None, error=None):
        self.llamadas = []
        self._respuesta, self._error = respuesta, error
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.llamadas.append(kwargs)
        if self._error:
            raise self._error
        return self._respuesta


def _respuesta(datos: dict, stop_reason="end_turn"):
    return SimpleNamespace(stop_reason=stop_reason, content=[SimpleNamespace(type="text", text=json.dumps(datos))])


_DATOS_IA = {
    "tipo": "documentos",
    "dependencia": "Secretaría de Planeación",
    "prioritario": False,
    "motivo_prioridad": "",
    "competencia_alcaldia": True,
    "asunto": "Certificado de uso del suelo",
    "peticionario": {"nombre": "Ana Ejemplo", "documento": "", "correo_respuesta": "", "direccion": ""},
    "confianza": 0.95,
}


def test_ia_usa_salida_estructurada_y_respaldo_del_servidor(catalogo):
    cliente = _ClienteFalso(_respuesta(_DATOS_IA))
    c = ClasificadorIA(catalogo, modelo="claude-opus-5-5", cliente=cliente).clasificar("texto")
    assert c.metodo == "ia" and c.dependencia == "Secretaría de Planeación"
    llamada = cliente.llamadas[0]
    assert llamada["output_config"]["format"]["type"] == "json_schema"
    assert llamada["fallbacks"] == "default"
    enum = llamada["output_config"]["format"]["schema"]["properties"]["dependencia"]["enum"]
    assert enum == catalogo.nombres_dependencias()


def test_ia_completa_correo_con_expresion_regular(catalogo):
    ia = ClasificadorIA(catalogo, cliente=_ClienteFalso(_respuesta(_DATOS_IA)))
    c = Clasificador(catalogo, ia).clasificar("Certificado de uso del suelo. Respuesta a ana@correo.ejemplo")
    assert c.peticionario.correo_respuesta == "ana@correo.ejemplo"


def test_si_la_ia_declina_usa_palabras_clave(catalogo):
    ia = ClasificadorIA(catalogo, cliente=_ClienteFalso(_respuesta(_DATOS_IA, stop_reason="refusal")))
    c = Clasificador(catalogo, ia).clasificar("Solicito paz y salvo del impuesto predial")
    assert c.metodo == "palabras_clave"
    assert c.dependencia == "Secretaría de Hacienda"


def test_si_no_hay_conexion_usa_palabras_clave(catalogo):
    error = anthropic.APIConnectionError(request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"))
    ia = ClasificadorIA(catalogo, cliente=_ClienteFalso(error=error))
    c = Clasificador(catalogo, ia).clasificar("Fuga de agua en el acueducto")
    assert c.metodo == "palabras_clave"
    assert c.dependencia == "Unidad de Servicios Públicos"
