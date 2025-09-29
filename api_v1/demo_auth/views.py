import secrets

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
    ):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password, 
    }


usernames_to_password = {
    "admin": "admin",
    "john": "password",
}

static_auth_token_username = {
    "3c4367c9c031516ffba34876bfb1": "admin",
    "24dc8a0e2ee14d8c4fc2ce8a5b55": "john",
}



def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    correct_password = usernames_to_password.get(credentials.username)

    if correct_password is None:
        raise unauthed_exc
    
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc
    
    return credentials.username


def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token"),
) -> str:
    if username := static_auth_token_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )
    

@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
    ):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }


@router.get("/some-http-header-auth-username/")
def demo_auth_http_header(
    username: str = Depends(get_username_by_static_auth_token),
    ):
    return {
        "message": f"Hi, {username}!",
        "username": username,
    }