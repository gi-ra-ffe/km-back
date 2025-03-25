# km-back/app/schemas.py
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from datetime import datetime

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

# 基本のアイテムスキーマ
class ItemBase(BaseModel):
    name : str
    category : str
    color : str
    memo : str = None  # メモ（任意）

# アイテム登録用のスキーマ
class ItemCreate(ItemBase):
    pass  # ItemBaseと同じ内容なので、そのまま継承

# アイテムレスポンス用のスキーマ
class ItemResponse(ItemBase):
    id: int  # タスクID
    created_at: datetime  # 作成日時
    updated_at: datetime  # 更新日時

    class Config:
        # ORM（データベースモデル）からデータを読み取る設定
        from_attributes = True

# 基本のコーディネートスキーマ
class CoordinateBase(BaseModel):
    name : str
    memo : str = None  # メモ（任意）

# コーディネート登録用のスキーマ
class CoordinateCreate(CoordinateBase):
    pass  # CoordinateBaseと同じ内容なので、そのまま継承

# コーディネートレスポンス用のスキーマ
class CoordinateResponse(CoordinateBase):
    id: int  # タスクID
    created_at: datetime  # 作成日時
    updated_at: datetime  # 更新日時
    class Config:
        # ORM（データベースモデル）からデータを読み取る設定
        from_attributes = True

# 基本のコーディネートアイテムスキーマ
class CoordinateItemsBase(BaseModel):
    day: datetime

# コーディネートアイテム登録用のスキーマ
class CoordinateItemsCreate(CoordinateItemsBase):
    pass  # CoordinateItemsBaseと同じ内容なので、そのまま継承

# コーディネートアイテムレスポンス用のスキーマ
class CoordinateItemsResponse(CoordinateItemsBase):
    id: int  # タスクID
    created_at: datetime  # 作成日時
    updated_at: datetime  # 更新日時
    item_id: int

    class Config:
        # ORM（データベースモデル）からデータを読み取る設定
        from_attributes = True