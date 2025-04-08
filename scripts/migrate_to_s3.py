import os
import boto3
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = "upload"
bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def migrate_images_to_s3():
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)

        # フォルダじゃなくて画像ファイルのみ対象
        if os.path.isfile(file_path):
            try:
                print(f"▶ アップロード中: {filename}")
                s3_client.upload_file(file_path, bucket_name, filename)
                print(f"✅ アップロード成功: {filename}")
                
                # オプション：ローカルから削除したい場合は以下を有効化
                # os.remove(file_path)
            except Exception as e:
                print(f"❌ アップロード失敗: {filename} - {e}")

if __name__ == "__main__":
    migrate_images_to_s3()
