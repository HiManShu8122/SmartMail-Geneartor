from app import create_app


class DummyResponse:
    output_text = "Subject: Hello\n\nHi there,\n\nGenerated email."


class DummyResponses:
    def create(self, **kwargs):
        self.kwargs = kwargs
        return DummyResponse()


class DummyClient:
    def __init__(self):
        self.responses = DummyResponses()


def test_index_loads():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"SmartMail Generator" in response.data


def test_generate_requires_topic():
    app = create_app()
    client = app.test_client()

    response = client.post("/generate", json={"topic": "", "tone": "professional"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Please provide an email topic."


def test_generate_returns_email(monkeypatch):
    monkeypatch.setattr("app.OpenAI", DummyClient)
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/generate",
        json={"topic": "Schedule a project kickoff", "tone": "friendly"},
    )

    assert response.status_code == 200
    assert "Generated email" in response.get_json()["email"]
