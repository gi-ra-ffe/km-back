from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Item, User, Coordinate , CoordinateItems
from app.schemas import ItemCreate, ItemResponse, CoordinateResponse
from app.database import get_db
from app.routes.auth import get_current_user
from app.routes.images import delete_file_if_exists, s3_client, bucket_name
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

    for item in items:
        if item.photo_url:
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': item.photo_url},
                ExpiresIn=3600
            )
            item.photo_url = presigned_url

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
def get_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムを取得
    """
    # 指定IDのアイテムを取得
    existing_item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if existing_item.photo_url:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': existing_item.photo_url},
            ExpiresIn=3600
        )
        existing_item.photo_url = presigned_url

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
    
    # 画像URLが変わっていたら古い画像削除
    if item.photo_url and item.photo_url != existing_item.photo_url:
        delete_file_if_exists(existing_item.photo_url)

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
    if item.photo_url:
        delete_file_if_exists(item.photo_url)
    db.delete(item)  # データを削除
    db.commit()  # 保存
    return {"message": "アイテムが削除されました"}

# 指定したアイテムを利用したコーディネート取得するエンドポイント
@router.get("/{item_id}/coordinates", response_model=List[CoordinateResponse],summary="アイテムを利用したコーディネートを取得",)
def get_coordinates_by_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムを利用したコーディネートを取得
    """
    coordinates = (
        db.query(Coordinate)
        .join(CoordinateItems)
        .filter(CoordinateItems.item_id == item_id)
        .filter(Coordinate.user_id == current_user.id)  # 自分のだけ
        .all()
    )

    for coordinate in coordinates:
        if coordinate.photo_url:
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': coordinate.photo_url},
                ExpiresIn=3600
            )
            coordinate.photo_url = presigned_url
    
    return [CoordinateResponse(**coordinate.__dict__) for coordinate in coordinates]  # dict から変換

# 指定したアイテムを利用したコーディネートから削除するエンドポイント
@router.delete("/{item_id}/coordinates",summary="指定したアイテムを利用したコーディネートから削除",)
def delete_item_from_coordinates(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムを利用したコーディネートから削除
    """
    items = (
        db.query(CoordinateItems)
        .join(Coordinate)
        .filter(CoordinateItems.item_id == item_id)
        .filter(Coordinate.user_id == current_user.id)
        .all()
    )
    if not items:
        return {"message": "削除対象のアイテムはありません"}

    for item in items:
        db.delete(item)
    
    db.commit()

    return {"message": f"{len(items)} 件のコーディネートからアイテムが削除されました"}