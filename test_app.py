
import pytest
import app as application


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_campusconnect.db"
    monkeypatch.setattr(application, "DATABASE", str(test_db))
    application.init_db()
    application.app.config["TESTING"] = True

    with application.app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TechFest 2026" in response.data


def test_add_event(client):
    response = client.post("/add", data={
        "name": "AI Workshop",
        "category": "Workshop",
        "date": "2026-12-10",
        "venue": "Lab 1",
        "description": "Learn AI",
        "capacity": "50"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"AI Workshop" in response.data


def test_register_for_event(client):
    with application.get_db() as db:
        event = db.execute(
            "SELECT id FROM events WHERE name = ?",
            ("TechFest 2026",)
        ).fetchone()

    assert event is not None
    event_id = event["id"]

    response = client.post(
        f"/register/{event_id}",
        follow_redirects=True
    )
    assert response.status_code == 200

    with application.get_db() as db:
        count = db.execute(
            "SELECT registrations FROM events WHERE id = ?",
            (event_id,)
        ).fetchone()["registrations"]

    assert count == 1


def test_invalid_event_capacity(client):
    response = client.post("/add", data={
        "name": "Invalid Event",
        "category": "Workshop",
        "date": "2026-12-10",
        "venue": "Lab 1",
        "capacity": "0"
    })

    assert response.status_code == 400
