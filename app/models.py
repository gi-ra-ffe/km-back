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
    # リレーション export
    items = relationship("Item", back_populates="user")
    coordinates = relationship("Coordinate", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    color = Column(String)
    memo = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(JST))  # 作成日時を現在時刻で自動設定
    updated_at = Column(DateTime, default=lambda: datetime.now(JST), onupdate=lambda: datetime.now(JST))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # リレーション import
    user = relationship("User", back_populates="items")
    # リレーション export
    coordinate_items = relationship("CoordinateItems", back_populates="item")

class Coordinate(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    day = Column(DateTime)
    memo = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(JST))  # 作成日時を現在時刻で自動設定
    updated_at = Column(DateTime, default=lambda: datetime.now(JST), onupdate=lambda: datetime.now(JST))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # リレーション import
    user = relationship("User", back_populates="coordinates")
    # リレーション export
    coordinate_items = relationship("CoordinateItems", back_populates="coordinate")

class CoordinateItems(Base):
    __tablename__ = "coordinate_items"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(JST))  # 作成日時を現在時刻で自動設定
    updated_at = Column(DateTime, default=lambda: datetime.now(JST), onupdate=lambda: datetime.now(JST))
    coordinate_id = Column(Integer, ForeignKey("coordinates.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    # リレーション import
    coordinate = relationship("Coordinate", back_populates="coordinate_items")
    item = relationship("Item", back_populates="coordinate_items")
    # リレーション export