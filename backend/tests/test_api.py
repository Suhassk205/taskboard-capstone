import pytest

def payload(**changes):
    return {"title":"Library Wi-Fi is unavailable","category":"IT","priority":"high",**changes}

def test_health(client):
    assert client.get("/health").json()=={"status":"healthy"}

def test_ready(client):
    assert client.get("/ready").json()=={"status":"ready"}

def test_create_and_read(client):
    created=client.post("/api/tickets",json=payload());assert created.status_code==201
    ticket=created.json();assert client.get(f"/api/tickets/{ticket['id']}").json()["title"]==payload()["title"]

def test_list(client):
    client.post("/api/tickets",json=payload())
    assert len(client.get("/api/tickets").json())==1

def test_update(client):
    ticket=client.post("/api/tickets",json=payload()).json()
    response=client.put(f"/api/tickets/{ticket['id']}",json=payload(status="resolved",owner="IT team"))
    assert response.status_code==200 and response.json()["status"]=="resolved"

def test_delete(client):
    ticket=client.post("/api/tickets",json=payload()).json()
    assert client.delete(f"/api/tickets/{ticket['id']}").status_code==204
    assert client.get(f"/api/tickets/{ticket['id']}").status_code==404

def test_stats(client):
    client.post("/api/tickets",json=payload(priority="urgent"))
    assert client.get("/api/tickets/stats").json()=={"total":1,"open":1,"in_progress":0,"resolved":0,"urgent":1}

def test_status_filter(client):
    client.post("/api/tickets",json=payload())
    client.post("/api/tickets",json=payload(status="resolved"))
    assert len(client.get("/api/tickets?status=resolved").json())==1

def test_search(client):
    client.post("/api/tickets",json=payload())
    assert len(client.get("/api/tickets?search=library").json())==1
    assert client.get("/api/tickets?search=missing").json()==[]

@pytest.mark.parametrize("changes",[{"title":""},{"priority":"invalid"},{"category":"Invalid"},{"status":"invalid"}])
def test_validation(client,changes):
    assert client.post("/api/tickets",json=payload(**changes)).status_code==422

def test_missing_ticket(client):
    assert client.get("/api/tickets/999").status_code==404

def test_metrics(client):
    client.get("/health")
    response=client.get("/metrics")
    assert response.status_code==200 and "http_requests_total" in response.text

def test_empty_database(client):
    assert client.get("/api/tickets").json()==[]
