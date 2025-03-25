# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, items
from app.database import Base, engine

# データベースの初期化
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURLを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを追加
app.include_router(auth.router)
app.include_router(items.router)

# @app.get("/api/todo")
# async def get_todos():
#     return [{"id": 1, "title": "Sample Task", "completed": False}]