from fastapi import APIRouter

from apis.varsion1 import route_users, route_jobs, route_login, route_posts,route_comments

api_router = APIRouter()

api_router.include_router(route_users.router,prefix="/user",tags=["users"])
#api_router.include_router(route_jobs.router,prefix="/job",tags=["jobs"])
api_router.include_router(route_login.router,prefix="/login",tags=["login"])
api_router.include_router(route_posts.router,prefix="/post",tags=["posts"])
api_router.include_router(route_comments.router,prefix="/comment",tags=["comments"])
