def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_route(client):
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/register", data=data)
    assert response.status_code == 200


def test_login_route(client):
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=data)
    assert response.status_code == 302


def test_logout_route(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_translate_route(client):
    client.post("/login", data={"username": "testuser", "password": "testpassword"})
    response = client.get("/translate")
    assert response.status_code == 200


def test_download_route(client):
    client.post("/login", data={"username": "testuser", "password": "testpassword"})
    response = client.get("/download")
    assert response.status_code == 200


def test_download_file_route(client):
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    filename = "example"
    response = client.get(f"/download/{filename}")
    assert response.status_code == 302
