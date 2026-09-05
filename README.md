# Baestargram Backend

Instagram 형태 React 프론트와 붙이는 FastAPI 백엔드입니다. 이 레포는 API만 관리합니다.

## 실행

Docker Desktop이 켜져 있어야 PostgreSQL이 뜹니다.

PowerShell (Windows):

```powershell
docker compose up -d

# C 드라이브가 가득 차면 pip/venv가 C:\Temp를 써서 실패합니다. E로 옮깁니다.
New-Item -ItemType Directory -Force -Path E:\tmp, E:\pip-cache | Out-Null
$env:TEMP = "E:\tmp"
$env:TMP = "E:\tmp"
$env:PIP_CACHE_DIR = "E:\pip-cache"

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

`source`는 Linux/Git Bash 명령입니다. PowerShell에서는 `.\.venv\Scripts\Activate.ps1`을 씁니다.
활성화가 막히면 활성화 없이 `.venv\Scripts\python.exe`로 실행해도 됩니다.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/health

React(Vite `5173` / CRA `3000`) CORS는 `.env`의 `CORS_ORIGINS`에서 맞춥니다.

프론트 `baseURL`은 `http://localhost:8000` 입니다.

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## PostgreSQL

로컬에 Postgres를 설치할 필요는 없습니다. Docker가 DB를 대신 띄웁니다.

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/)을 설치하고 실행합니다.
2. 프로젝트에서 `docker compose up -d`를 실행합니다.
3. `localhost:5432`에 `baestargram / baestargram` DB가 생깁니다.

데이터는 C가 아니라 `E:\baestargram_backend\data\postgres`에 저장됩니다.

앱은 `.env`의 `DATABASE_URL`로 접속합니다.

```
postgresql+psycopg://baestargram:baestargram@localhost:5432/baestargram
```

Docker 없이 쓰려면 Postgres 설치 경로를 `E:\PostgreSQL`로 지정한 뒤, 위 계정/DB만 만들면 됩니다.

```sql
CREATE USER baestargram WITH PASSWORD 'baestargram';
CREATE DATABASE baestargram OWNER baestargram;
```

## Alembic

테이블은 앱 시작이 아니라 마이그레이션으로 만듭니다.

```powershell
docker compose up -d
.\.venv\Scripts\python.exe -m alembic upgrade head
```

모델 바꾼 뒤:

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "add something"
.\.venv\Scripts\python.exe -m alembic upgrade head
```

## 인증 API

프론트가 기대하는 계약:

`POST /auth/signup`

```json
{ "username": "baestar", "email": "baestar@example.com", "password": "password123", "display_name": "Bae Star" }
```

`POST /auth/login`

```json
{ "username": "baestar", "password": "password123" }
```

둘 다 응답:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "baestar",
    "email": "baestar@example.com",
    "display_name": "Bae Star"
  }
}
```

로그인 `username`에는 이메일도 넣을 수 있습니다.

## 구조

```
app/
  main.py              FastAPI 앱, CORS, /uploads 마운트
  core/                설정, JWT, 인증 의존성
  db/                  SQLAlchemy 엔진/세션
  models/              User, Post, Comment, Like, Follow, Story
  schemas/             요청/응답 DTO
  api/v1/endpoints/    라우트만 담당
  services/            비즈니스 로직
  utils/               로컬 미디어 저장
alembic/               마이그레이션
docker-compose.yml     로컬 PostgreSQL
```

레이어는 `router -> service -> model` 입니다.

## 그 외 API

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/auth/me` | 내 정보 |
| GET | `/api/v1/users/{username}` | 프로필 조회 |
| PATCH | `/api/v1/users/me` | 프로필 수정 |

경로만 잡아 둔 것 (쓰기는 `501`):

- 게시물 `/api/v1/posts`
- 댓글 `/api/v1/posts/{post_id}/comments`
- 좋아요 `/api/v1/posts/{post_id}/like`
- 팔로우 `/api/v1/users/{username}/follow`
- 피드 `/api/v1/feed`
- 스토리 `/api/v1/stories`
