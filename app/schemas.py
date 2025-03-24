# km-back/app/schemas.py
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

# パスワード用の正規表現パターン
PASSWORD_PATTERN = r"^[a-zA-Z0-9!-/:-@\[-`{-~]*$"

# ユーザー登録用のスキーマ
class UserCreate(BaseModel):
    username: str  # ユーザー名
    email: EmailStr  # メールアドレス（形式チェック付き）
    password: str

    class Config:
        from_attributes = True

    # パスワードは英数字のみとする
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not re.match(PASSWORD_PATTERN, v):
            raise ValueError("パスワードは半角英数字と記号のみ使用できます")
        return v

# ユーザーログイン用のスキーマ
class UserLogin(BaseModel):
    email: EmailStr  # メールアドレス（形式チェック付き）
    password: str

    class Config:
        from_attributes = True