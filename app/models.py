from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime, timezone, timedelta

# JSTタイムゾーンを定義
JST = timezone(timedelta(hours=9))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(JST))  # 作成日時を現在時刻で自動設定
    updated_at = Column(DateTime, default=lambda: datetime.now(JST), onupdate=lambda: datetime.now(JST))