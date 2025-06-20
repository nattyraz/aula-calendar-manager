import pytest
from unittest.mock import Mock, patch
from app.aula_client import AulaApiClient

@pytest.fixture
def aula_client():
    return AulaApiClient("test_user", "test_pass")

@pytest.mark.asyncio
async def test_aula_client_initialization(aula_client):
    """Test l'initialisation du client Aula"""
    assert aula_client.username == "test_user"
    assert aula_client.password == "test_pass"
    assert aula_client.logged_in == False
    assert aula_client.children == []
    assert aula_client.institutions == []

@pytest.mark.asyncio
async def test_login_success(aula_client):
    """Test de connexion r?ussie (mocked)"""
    # Ce test n?cessite de mocker aiohttp
    # Pour l'instant, test basique
    assert hasattr(aula_client, 'login')

def test_context_manager(aula_client):
    """Test du context manager"""
    assert hasattr(aula_client, '__aenter__')
    assert hasattr(aula_client, '__aexit__')