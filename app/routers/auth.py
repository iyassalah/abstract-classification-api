"""Module to handle auth"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt

from ..config import settings
from ..crud import authenticate_user, create_user, get_user
from ..dependancies import Token, TokenData, create_access_token, oauth2_scheme
from ..models import User

router = APIRouter(tags=["auth"], prefix="/auth")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Fetches the current user using the information in the recieve JWT, validates JWT.

    Args:
        token (`Annotated[str, Depends`): JWT token containing username and expiry date

    Raises:
        HTTPException: If JWT is invalid with code 401
        HTTPException: If JWT is expired with code 403

    Returns:
        `User`: The user account associated with the JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="token has expired") from None
    except JWTError:
        raise credentials_exception from None
    if not token_data.username:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def require_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    """Fetches the current user using the information in the recieve JWT, validates JWT.

    Args:
        token (`Annotated[str, Depends`): JWT token containing username and expiry date

    Raises:
        HTTPException: If JWT is invalid with code 401
        HTTPException: If JWT is expired with code 403

    Returns:
        `User`: The user account associated with the JWT
    """
    user = await get_current_user(token)
    if not user["isAdmin"]:
        raise HTTPException(
            status_code=403, detail="Insufficient permissions"
        ) from None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Creates a token using OAuth2

    Args:
        form_data (`OAuth2PasswordRequestForm`): _description_

    Raises:
        HTTPException: If the username or password are not valid

    Returns:
        `dict`: contains `token_type` and `access_token`
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role = "admin" if user["isAdmin"] else "none"
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create", response_model=Token)
async def add_user(form_data: User):
    """Create a new user with the given user data, generate a new access token
    and add it to the user's tokens.

    Args:
        form_data (User): The user data to be used for creating the new user.

    Returns:
        Token: The generated access token.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    create_user(
        {
            "username": form_data.username,
            "email": form_data.email,
            "isAdmin": False,
            "password": form_data.password,
            "token": [access_token],
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
