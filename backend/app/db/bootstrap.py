from sqlalchemy import select

from app.core.config import Settings
from app.core.security import hash_password
from app.db.models import User
from app.db.session import SessionLocal


def bootstrap_admin(settings: Settings) -> None:
    """Create the initial admin account from environment variables if absent.

    The bootstrap credentials are never written to source control. An existing
    account is left untouched so a redeploy cannot overwrite a changed password.
    """
    email = settings.admin_email.strip().lower() if settings.admin_email else ""
    password = settings.admin_password or ""

    if not email and not password:
        return
    if not email or not password:
        raise RuntimeError("ADMIN_EMAIL and ADMIN_PASSWORD must be provided together")
    if len(password) < 12:
        raise RuntimeError("ADMIN_PASSWORD must be at least 12 characters")

    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.email == email))
        if existing:
            return

        db.add(
            User(
                email=email,
                password_hash=hash_password(password),
                role="admin",
                is_active=True,
                must_change_password=True,
            )
        )
        db.commit()
