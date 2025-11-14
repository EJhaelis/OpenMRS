import pytest
from utils.config import BASIC_TOKEN
@pytest.fixture(scope="session")
def auth_headers():
    """
    Devuelve un diccionario de headers con token válido.
    Útil para reutilizar en cualquier test que requiera autenticación.
    """
    token = BASIC_TOKEN
    return {'Authorization': f'Basic {token}'}