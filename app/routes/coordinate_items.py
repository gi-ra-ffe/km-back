from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import CoordinateItems, User
from app.schemas import CoordinateItemsCreate, CoordinateItemsResponse
from app.database import get_db
from app.routes.auth import get_current_user
from typing import List

# ルーターの作成（エンドポイントのプレフィックスとタグを設定）
router = APIRouter(prefix="/coordinate_items", tags=["coordinateItems"])

# 指定したコーディネートIDに紐づくアイテム一覧を取得するエンドポイント
@router.get("", response_model=List[CoordinateItemsResponse],summary="指定したIDのコーディネートに使用したアイテム一覧を取得",)
def get_coordinateItems(coordinate_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したコーディネートIDに紐づくアイテムを全て取得
    """
    coordinateItems = db.query(CoordinateItems).filter(CoordinateItems.coordinate_id == coordinate_id).all()
    return [CoordinateItemsResponse(**coordinate.__dict__) for coordinate in coordinateItems]  # dict から変換

# コーディネートに使用したアイテムを登録するエンドポイント
@router.post("", response_model=List[CoordinateItemsResponse],summary="コーディネートに使用したアイテムを登録",)
def create_coordinateItems(
    coordinateItems: CoordinateItemsCreate , 
    coordinate_id: int,
    used_items: list[int],
    db: Session = Depends(get_db), 
    ):
    """
    新しいコーディネートに使用したアイテムを登録
    """
    created = []

    for item_id in used_items:
        new_item = CoordinateItems(
            item_id=item_id,
            coordinate_id=coordinate_id,
            day=coordinateItems.day
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        created.append(new_item)

    return [CoordinateItemsResponse.model_validate(item) for item in created]

# コーディネートに使用したアイテムを更新するエンドポイント
@router.put("/{coordinate_id}", response_model=List[CoordinateItemsResponse],summary="コーディネートに使用したアイテムを更新",)
def update_coordinateItems(
    coordinateItems: CoordinateItemsCreate , 
    coordinate_id: int, 
    used_items: list[int],
    db: Session = Depends(get_db), 
    ):
    """
    指定したIDのコーディネートに使用したアイテムを更新
    """

    db.query(CoordinateItems).filter(CoordinateItems.coordinate_id == coordinate_id).delete()

    updated = []

    for item_id in used_items:
        new_item = CoordinateItems(
            item_id=item_id,
            coordinate_id=coordinate_id,
            day=coordinateItems.day
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        updated.append(new_item)

    return [CoordinateItemsResponse.model_validate(item) for item in updated]

# アイテムをコーディネートから削除するエンドポイント
@router.delete("/{coordinate_id}",summary="アイテムをコーディネートから削除",)
def delete_coordinateItems(coordinate_id: int, db: Session = Depends(get_db)):
    """
    指定したIDのアイテムをコーディネートから削除
    """
    
    coordinate = db.query(CoordinateItems).filter(CoordinateItems.id == coordinate_id).first()
    if not coordinate:
        raise HTTPException(status_code=404, detail="CoordinateItems not found")
    db.query(CoordinateItems).filter(CoordinateItems.coordinate_id == coordinate_id).delete()  # データを削除
    db.commit()  # 保存
    return {"message": "コーディネートに使用したアイテムが削除されました"}