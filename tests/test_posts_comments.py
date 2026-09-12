def _signup(client, username="writer", email="writer@example.com"):
    response = client.post(
        "/auth/signup",
        json={
            "username": username,
            "email": email,
            "password": "password123",
            "display_name": "Writer",
        },
    )
    assert response.status_code == 201
    body = response.json()
    return {"Authorization": f"Bearer {body['access_token']}"}, body["user"]


def test_create_post_and_comment(client):
    headers, user = _signup(client)

    created = client.post(
        "/api/v1/posts",
        json={
            "caption": "첫 게시물",
            "media_urls": ["https://example.com/photo.jpg"],
        },
        headers=headers,
    )
    assert created.status_code == 201
    post = created.json()
    assert post["caption"] == "첫 게시물"
    assert post["author"]["username"] == user["username"]
    assert post["media"][0]["url"] == "https://example.com/photo.jpg"
    assert post["comment_count"] == 0

    comment = client.post(
        f"/api/v1/posts/{post['id']}/comments",
        json={"content": "멋져요"},
        headers=headers,
    )
    assert comment.status_code == 201
    assert comment.json()["content"] == "멋져요"
    assert comment.json()["author"]["username"] == user["username"]

    listed = client.get(f"/api/v1/posts/{post['id']}/comments")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    feed = client.get("/api/v1/feed", headers=headers)
    assert feed.status_code == 200
    assert feed.json()[0]["id"] == post["id"]
    assert feed.json()[0]["comment_count"] == 1


def test_reply_nests_under_root_comment(client):
    headers, _ = _signup(client, username="replier", email="replier@example.com")
    post = client.post(
        "/api/v1/posts",
        json={"caption": "답글", "media_urls": ["https://example.com/a.jpg"]},
        headers=headers,
    ).json()

    root = client.post(
        f"/api/v1/posts/{post['id']}/comments",
        json={"content": "원댓글"},
        headers=headers,
    ).json()
    reply = client.post(
        f"/api/v1/posts/{post['id']}/comments",
        json={"content": "대댓글", "parent_id": root["id"]},
        headers=headers,
    ).json()
    nested = client.post(
        f"/api/v1/posts/{post['id']}/comments",
        json={"content": "대댓글의 답글", "parent_id": reply["id"]},
        headers=headers,
    ).json()

    assert reply["parent_id"] == root["id"]
    assert nested["parent_id"] == root["id"]

    listed = client.get(f"/api/v1/posts/{post['id']}/comments").json()
    assert [item["content"] for item in listed] == ["원댓글", "대댓글", "대댓글의 답글"]


def test_comment_requires_existing_post(client):
    headers, _ = _signup(client, username="cmtuser", email="cmt@example.com")
    missing = client.post(
        "/api/v1/posts/999/comments",
        json={"content": "없는 글"},
        headers=headers,
    )
    assert missing.status_code == 404


def test_upload_image_and_create_post(client, tmp_path, monkeypatch):
    from app.utils import storage

    monkeypatch.setattr(storage.settings, "UPLOAD_DIR", str(tmp_path))
    headers, _ = _signup(client, username="uploader", email="up@example.com")

    upload = client.post(
        "/api/v1/uploads",
        files={"file": ("cat.png", b"\x89PNG\r\n\x1a\n" + b"0" * 32, "image/png")},
        headers=headers,
    )
    assert upload.status_code == 200
    url = upload.json()["url"]
    assert url.startswith("/uploads/")

    created = client.post(
        "/api/v1/posts",
        json={"caption": "업로드", "media_urls": [url]},
        headers=headers,
    )
    assert created.status_code == 201
    assert created.json()["media"][0]["url"] == url


def test_like_and_unlike_post(client):
    owner_headers, _ = _signup(client, username="owner", email="owner@example.com")
    fan_headers, _ = _signup(client, username="fan", email="fan@example.com")
    post = client.post(
        "/api/v1/posts",
        json={"caption": "좋아요", "media_urls": ["https://example.com/like.jpg"]},
        headers=owner_headers,
    ).json()

    liked = client.post(f"/api/v1/posts/{post['id']}/like", headers=fan_headers)
    assert liked.status_code == 200
    assert liked.json() == {"liked": True, "like_count": 1}

    again = client.post(f"/api/v1/posts/{post['id']}/like", headers=fan_headers)
    assert again.status_code == 200
    assert again.json()["like_count"] == 1

    feed = client.get("/api/v1/feed", headers=fan_headers).json()
    assert feed[0]["liked_by_me"] is True
    assert feed[0]["like_count"] == 1

    unliked = client.delete(f"/api/v1/posts/{post['id']}/like", headers=fan_headers)
    assert unliked.status_code == 200
    assert unliked.json() == {"liked": False, "like_count": 0}
