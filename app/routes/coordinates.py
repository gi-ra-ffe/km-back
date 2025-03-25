from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Coordinate, User
from app.schemas import CoordinateCreate, CoordinateResponse
from app.database import get_db
from app.routes.auth import get_current_user
from typing import List

# ルーターの作成（エンドポイントのプレフィックスとタグを設定）
router = APIRouter(prefix="/coordinates", tags=["coordinates"])

# コーディネート一覧を取得するエンドポイント
@router.get("", response_model=List[CoordinateResponse],summary="コーディネート一覧を取得",)
def get_coordinates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    現在のユーザーに紐づくコーディネートを全て取得
    """
    coordinates = db.query(Coordinate).filter(Coordinate.user_id == current_user.id).all()
    return [CoordinateResponse(**coordinate.__dict__) for coordinate in coordinates]  # dict から変換

# コーディネートを作成するエンドポイント
@router.post("", response_model=CoordinateResponse,summary="コーディネートを作成",)
def create_coordinate(coordinate: CoordinateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    新しいコーディネートを作成
    """
    # Coordinateモデルにスキーマのデータを詰めて新規作成
    new_coordinate = Coordinate(**coordinate.dict(), user_id=current_user.id)
    db.add(new_coordinate)  # データベースに追加
    db.commit()  # 変更を保存
    db.refresh(new_coordinate)  # 新しいデータをリロード
    return CoordinateResponse(**new_coordinate.__dict__)

# コーディネートを更新するエンドポイント
@router.put("/{coordinate_id}", response_model=CoordinateResponse,summary="コーディネートを更新",)
def update_coordinate(coordinate_id: int, coordinate: CoordinateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのコーディネートを更新
    """
    # 指定IDのコーディネートを取得
    existing_coordinate = db.query(Coordinate).filter(Coordinate.id == coordinate_id, Coordinate.user_id == current_user.id).first()
    if not existing_coordinate:
        raise HTTPException(status_code=404, detail="Coordinate not found")
    # 更新するフィールドを設定
    for key, value in coordinate.dict(exclude_unset=True).items():
        setattr(existing_coordinate, key, value)
    db.commit()  # 保存
    db.refresh(existing_coordinate)  # データをリロード
    return CoordinateResponse(**existing_coordinate.__dict__)

# コーディネートを削除するエンドポイント
@router.delete("/{coordinate_id}",summary="コーディネートを削除",)
def delete_coordinate(coordinate_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    指定したIDのコーディネートを削除
    """
    coordinate = db.query(Coordinate).filter(Coordinate.id == coordinate_id, Coordinate.user_id == current_user.id).first()
    if not coordinate:
        raise HTTPException(status_code=404, detail="Coordinate not found")
    db.delete(coordinate)  # データを削除
    db.commit()  # 保存
    return {"message": "コーディネートが削除されました"}