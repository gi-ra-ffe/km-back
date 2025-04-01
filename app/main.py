# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, items, coordinates, coordinate_items, images
from app.database import Base, engine

# データベースの初期化
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS の設定
origins = [
    "http://localhost",  # フロントエンドが動作しているドメイン
    "http://192.168.11.2:3000",  # 必要に応じて他のオリジンも追加
]

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # フロントエンドのURLを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを追加
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(coordinates.router)
app.include_router(coordinate_items.router)
app.include_router(images.router)

# # 静的ファイル（画像など）の公開設定
app.mount("/images", StaticFiles(directory="upload"), name="images")