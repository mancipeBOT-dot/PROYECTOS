import pytest

from ventanilla.catalogo import Catalogo
from ventanilla.clasificador import Clasificador
from ventanilla.servicio import Ventanilla


@pytest.fixture
def catalogo() -> Catalogo:
    return Catalogo.desde_archivo()


@pytest.fixture
def ventanilla(catalogo) -> Ventanilla:
    return Ventanilla(catalogo, Clasificador(catalogo))
