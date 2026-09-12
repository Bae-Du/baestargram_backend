from app.utils.profanity import PROFANITY_MESSAGE, contains_profanity


def test_detects_english_and_korean_profanity():
    assert contains_profanity("what the fuck")
    assert contains_profanity("f u c k")
    assert contains_profanity("sh1t happens")
    assert contains_profanity("진짜 시발")
    assert contains_profanity("시 발 진짜")


def test_allows_normal_words():
    assert not contains_profanity("hello class assistant")
    assert not contains_profanity("오늘 날씨 좋다")
    assert not contains_profanity("")
    assert not contains_profanity(None)


def test_signup_and_comment_reject_profanity(client):
    blocked = client.post(
        "/auth/signup",
        json={
            "username": "fuckuser",
            "email": "fuckuser@example.com",
            "password": "password123",
        },
    )
    assert blocked.status_code == 400
    assert blocked.json()["detail"] == PROFANITY_MESSAGE

    ok = client.post(
        "/auth/signup",
        json={
            "username": "cleanuser",
            "email": "cleanuser@example.com",
            "password": "password123",
        },
    )
    assert ok.status_code == 201
    token = ok.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    post = client.post(
        "/api/v1/posts",
        json={"caption": "ok", "media_urls": ["https://example.com/a.jpg"]},
        headers=headers,
    )
    assert post.status_code == 201

    comment = client.post(
        f"/api/v1/posts/{post.json()['id']}/comments",
        json={"content": "시발"},
        headers=headers,
    )
    assert comment.status_code == 400
    assert comment.json()["detail"] == PROFANITY_MESSAGE
