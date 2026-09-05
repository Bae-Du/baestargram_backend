from fastapi import APIRouter, status

from app.core.deps import CurrentUser, DBSession
from app.schemas.auth import AuthResponse, LoginRequest, SignupRequest
from app.schemas.user import UserMe
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: DBSession) -> AuthResponse:
    return auth_service.signup_user(db, payload)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: DBSession) -> AuthResponse:
    return auth_service.login_user(db, payload)


@router.get("/me", response_model=UserMe)
def me(current_user: CurrentUser) -> UserMe:
    return current_user
