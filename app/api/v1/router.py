from fastapi import APIRouter

from app.api.v1.endpoints import comments, feed, likes, posts, stories, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(posts.router)
api_router.include_router(comments.router)
api_router.include_router(likes.router)
api_router.include_router(feed.router)
api_router.include_router(stories.router)
