from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Item, User
from app.schemas import ItemCreate, ItemResponse
from app.database import get_db
from app.routes.auth import get_current_user
from typing import List

# ルーターの作成（エンドポイントのプレフィックスとタグを設定）
router = APIRouter(prefix="/items", tags=["items"])

# アイテム一覧を取得するエンドポイント
@router.get("", response_model=List[ItemResponse],summary="アイテム一覧を取得",)
def get_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    現在のユーザーに紐づくアイテムを全て取得
    """
    items = db.query(Item).filter(Item.user_id == current_user.id).all()
    return [ItemResponse(**item.__dict__) for item in items]  # dict から変換

# アイテムを作成するエンドポイント
@router.post("", response_model=ItemResponse,summary="アイテムを作成",)
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    新しいアイテムを作成
    """
    # Itemモデルにスキーマのデータを詰めて新規作成
    new_item = Item(**item.dict(), user_id=current_user.id)
    db.add(new_item)  # データベースに追加
    db.commit()  # 変更を保存
    db.refresh(new_item)  # 新しいデータをリロード
    return ItemResponse(**new_item.__dict__)

# アイテムを取得するエンドポイント
@router.get("/{item_id}", response_model=ItemResponse,summary="アイテムを取得",)
def update_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムを取得
    """
    # 指定IDのアイテムを取得
    existing_item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(**existing_item.__dict__)

# アイテムを更新するエンドポイント
@router.put("/{item_id}", response_model=ItemResponse,summary="アイテムを更新",)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムを更新
    """
    # 指定IDのアイテムを取得
    existing_item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")
    # 更新するフィールドを設定
    for key, value in item.dict(exclude_unset=True).items():
        setattr(existing_item, key, value)
    db.commit()  # 保存
    db.refresh(existing_item)  # データをリロード
    return ItemResponse(**existing_item.__dict__)

# アイテムを削除するエンドポイント
@router.delete("/{item_id}",summary="アイテムを削除",)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムを削除
    """
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)  # データを削除
    db.commit()  # 保存
    return {"message": "アイテムが削除されました"}