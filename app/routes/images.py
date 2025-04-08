# km-back/app/routes/images.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from PIL import Image
from app.models import User
from app.routes.auth import get_current_user
import os
import io
import boto3
from datetime import datetime

# ルーターの作成（エンドポイントのプレフィックスとタグを設定）
router = APIRouter(prefix="/images", tags=["images"])

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".heic"}

bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def validate_image_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="対応していないファイル形式です")
    
def delete_file_if_exists(filename: str):
    if not filename:
        return
    try:
        # S3にオブジェクトがあるか確認
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=filename)
        if 'Contents' in response:
            s3_client.delete_object(Bucket=bucket_name, Key=filename)
            print(f"🗑 削除成功: {filename}")
        else:
            print(f"⚠️ 削除スキップ（存在しない）: {filename}")
    except Exception as e:
        print(f"❌ 削除失敗: {e}")

def generate_presigned_url(filename: str):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': filename},
        ExpiresIn=3600
    )
    return {"photo_url": url}
    
# 画像をアップロードするエンドポイント
@router.post("",summary="画像をアップロード",)
def upload_image(uploaded_file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    try:
        validate_image_file(uploaded_file)
        image = Image.open(uploaded_file.file).convert("RGB")
        filename = f"user{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

        # メモリ上にJPEGとして保存
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)  # 書き込み位置を先頭に戻す

        s3_client.upload_fileobj(buffer, bucket_name, filename)
        print(f"File {uploaded_file} uploaded to {bucket_name}/{filename}")
        
        # 保存後のURLを返す
        return {"photo_url": filename}
    except Exception as e:
        return {"error": str(e)}