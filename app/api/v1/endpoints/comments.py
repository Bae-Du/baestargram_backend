from fastapi import APIRouter, status

from app.core.deps import CurrentUser, DBSession
from app.schemas.comment import CommentCreate, CommentRead
from app.services import comment as comment_service

router = APIRouter(tags=["comments"])


@router.get("/posts/{post_id}/comments", response_model=list[CommentRead])
def list_comments(post_id: int, db: DBSession) -> list[CommentRead]:
    return comment_service.list_comments(db, post_id)


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> CommentRead:
    return comment_service.create_comment(db, post_id, current_user, payload)
