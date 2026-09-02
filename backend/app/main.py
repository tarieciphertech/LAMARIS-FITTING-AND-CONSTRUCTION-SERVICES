from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.api.routes import auth, enquiries, properties
from app.core.config import get_settings
from app.db import models
from app.db.session import Base, engine

settings = get_settings()

app = FastAPI(title="Lamaris Property Platform API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(auth.router, prefix="/api")
app.include_router(properties.router, prefix="/api")
app.include_router(enquiries.router, prefix="/api")


@app.get("/api/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "service": "lamaris-api"}


try:
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
except RuntimeError:
    pass
