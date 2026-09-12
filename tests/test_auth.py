def test_signup_and_login(client):
    signup = client.post(
        "/auth/signup",
        json={
            "username": "baestar",
            "email": "baestar@example.com",
            "password": "password123",
            "display_name": "Bae Star",
        },
    )
    assert signup.status_code == 201
    signup_body = signup.json()
    assert signup_body["token_type"] == "bearer"
    assert signup_body["user"]["username"] == "baestar"
    assert signup_body["user"]["display_name"] == "Bae Star"
    assert signup_body["access_token"]

    login = client.post(
        "/auth/login",
        json={"username": "baestar", "password": "password123"},
    )
    assert login.status_code == 200
    login_body = login.json()
    token = login_body["access_token"]
    assert login_body["user"]["email"] == "baestar@example.com"

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "baestar@example.com"


def test_signup_defaults_display_name_to_username(client):
    signup = client.post(
        "/auth/signup",
        json={
            "username": "nonameuser",
            "email": "noname@example.com",
            "password": "password123",
        },
    )
    assert signup.status_code == 201
    assert signup.json()["user"]["display_name"] == "nonameuser"

    empty_name = client.post(
        "/auth/signup",
        json={
            "username": "emptyname",
            "email": "emptyname@example.com",
            "password": "password123",
            "display_name": "   ",
        },
    )
    assert empty_name.status_code == 201
    assert empty_name.json()["user"]["display_name"] == "emptyname"
