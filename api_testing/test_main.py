from fastapi.testclient import TestClient

from api_testing.main import app

client = TestClient(app)

# testing home API
def test_home():
    response = client.get("/")
    # check for status code
    assert response.status_code == 200
    # check for data
    assert response.json()=={
        "message":"Hello! Welcome back"
    }

    # testing the Add api

    def test_add():
        response = client.get("/add?a=3&b=5")
        assert response.status_code ==200
        assert response.json() =={
            "sum":8
        }