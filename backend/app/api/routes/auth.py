from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.db.models import User
from app.db.session import get_db
from app.schemas import ChangePasswordRequest, LoginRequest, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if not user or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenOut(
        access_token=create_access_token(user),
        must_change_password=user.must_change_password,
    )


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "must_change_password": user.must_change_password}


@router.post("/change-password", response_model=TokenOut)
def change_password(
    payload: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    if verify_password(payload.new_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different")

    user.password_hash = hash_password(payload.new_password)
    user.must_change_password = False
    user.token_version += 1
    db.commit()
    db.refresh(user)

    return TokenOut(
        access_token=create_access_token(user),
        must_change_password=False,
    )


@router.post("/logout")
def logout(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # JWTs are stateless; incrementing the version invalidates the current token
    # and any other active tokens for this user. The client should also remove its token.
    user.token_version += 1
    db.commit()
    return {"message": "Logged out successfully"}
