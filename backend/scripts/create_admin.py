import getpass
import os
import sys

from sqlalchemy import select

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.security import hash_password
from app.db.models import User
from app.db.session import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)
email = input("Admin email: ").strip().lower()
password = getpass.getpass("Admin password: ")
confirmation = getpass.getpass("Confirm password: ")

if not email or len(password) < 12:
    raise SystemExit("Use a valid email and a password of at least 12 characters.")
if password != confirmation:
    raise SystemExit("Passwords do not match.")

with SessionLocal() as db:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        user.password_hash = hash_password(password)
        user.is_active = True
        user.must_change_password = False
        print(f"Updated admin account: {email}")
    else:
        db.add(User(email=email, password_hash=hash_password(password), is_active=True, must_change_password=False))
        print(f"Created admin account: {email}")
    db.commit()
