import pytest


def test_pytest_funcionando():
    """Confirma que o pytest encontrou e executou este arquivo."""
    assert 1 + 1 == 2


@pytest.mark.smoke
def test_raiz_retorna_200(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.smoke
def test_raiz_contem_mensagem(client):
    data = client.get("/").json()
    assert "mensagem" in data
    assert "Bella Tavola" in data["mensagem"]
