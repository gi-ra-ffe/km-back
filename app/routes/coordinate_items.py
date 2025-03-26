from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import CoordinateItems, Coordinate, User
from app.schemas import CoordinateItemsCreate, CoordinateItemsResponse
from app.database import get_db
from app.routes.auth import get_current_user
from typing import List

# ルーターの作成（エンドポイントのプレフィックスとタグを設定）
router = APIRouter(prefix="/coordinate_items", tags=["coordinateItems"])

# コーディネートに使用したアイテムを登録するエンドポイント
@router.post("", response_model=List[CoordinateItemsResponse],summary="コーディネートに使用したアイテムを登録",)
def create_coordinateItems(
    coordinateItems: CoordinateItemsCreate , 
    coordinate_id: int,
    used_items: list[int],
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    """
    新しいコーディネートに使用したアイテムを登録
    """
    # coordinate を取得
    coordinate = db.query(Coordinate).filter(Coordinate.id == coordinate_id).first()

    if not coordinate:
        raise HTTPException(status_code=404, detail="コーディネートが見つかりません")

    # ログインユーザーのIDと一致するかチェック
    if coordinate.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="このコーディネートへのアクセス権がありません")
    
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

# 指定したコーディネートIDに紐づくアイテム一覧を取得するエンドポイント
@router.get("/{coordinate_id}", response_model=List[CoordinateItemsResponse],summary="指定したIDのコーディネートに使用したアイテム一覧を取得",)
def get_coordinateItems(coordinate_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したコーディネートIDに紐づくアイテムを全て取得
    """
    # coordinate を取得
    coordinate = db.query(Coordinate).filter(Coordinate.id == coordinate_id).first()

    if not coordinate:
        raise HTTPException(status_code=404, detail="コーディネートが見つかりません")

    # ログインユーザーのIDと一致するかチェック
    if coordinate.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="このコーディネートへのアクセス権がありません")

    coordinateItems = db.query(CoordinateItems).filter(CoordinateItems.coordinate_id == coordinate_id).all()
    return [CoordinateItemsResponse(**coordinateItem.__dict__) for coordinateItem in coordinateItems]  # dict から変換

# コーディネートに使用したアイテムを更新するエンドポイント
@router.put("/{coordinate_id}", response_model=List[CoordinateItemsResponse],summary="コーディネートに使用したアイテムを更新",)
def update_coordinateItems(
    coordinateItems: CoordinateItemsCreate , 
    coordinate_id: int, 
    used_items: list[int],
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    """
    指定したIDのコーディネートに使用したアイテムを更新
    """
    # coordinate を取得
    coordinate = db.query(Coordinate).filter(Coordinate.id == coordinate_id).first()

    if not coordinate:
        raise HTTPException(status_code=404, detail="コーディネートが見つかりません")

    # ログインユーザーのIDと一致するかチェック
    if coordinate.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="このコーディネートへのアクセス権がありません")

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
def delete_coordinateItems(coordinate_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    """
    指定したIDのアイテムをコーディネートから削除
    """
    # coordinate を取得
    coordinate = db.query(Coordinate).filter(Coordinate.id == coordinate_id).first()

    if not coordinate:
        raise HTTPException(status_code=404, detail="コーディネートが見つかりません")

    # ログインユーザーのIDと一致するかチェック
    if coordinate.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="このコーディネートへのアクセス権がありません")
    
    db.query(CoordinateItems).filter(CoordinateItems.coordinate_id == coordinate_id).delete()  # データを削除
    db.commit()  # 保存
    return {"message": "コーディネートに使用したアイテムが削除されました"}