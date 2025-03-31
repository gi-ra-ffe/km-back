# km-back/app/routes/images.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from PIL import Image
from app.models import User
from app.routes.auth import get_current_user
import os
from datetime import datetime

# ルーターの作成（エンドポイントのプレフィックスとタグを設定）
router = APIRouter(prefix="/images", tags=["images"])

UPLOAD_DIR = "upload/"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".heic"}

def validate_image_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="対応していないファイル形式です")
    
def delete_file_if_exists(photo_url: str):
    if photo_url:
        file_path = os.path.join("upload", os.path.basename(photo_url))
        if os.path.exists(file_path):
            os.remove(file_path)
    
# 画像URLを作成するエンドポイント
@router.post("",summary="画像URLを作成",)
def upload_image(uploaded_file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    try:
        validate_image_file(uploaded_file)
        image = Image.open(uploaded_file.file).convert("RGB")
        filename = f"user{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        path = os.path.join(UPLOAD_DIR, filename)
        image.save(path, "JPEG")

        # 保存後のURLを返す
        return {"photo_url": f"/images/{filename}"}
    except Exception as e:
        return {"error": str(e)}