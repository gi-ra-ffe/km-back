# scripts/migrate_sqlite_to_postgre.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import User, Item, Coordinate, CoordinateItems 
from dotenv import load_dotenv
import os

# SQLiteの設定
sqlite_engine = create_engine("sqlite:///./km_app.db", connect_args={"check_same_thread": False})
SQLiteSession = sessionmaker(bind=sqlite_engine)

# .env ファイルを明示的に読み込む
load_dotenv()
# 接続URLを取得
DATABASE_URL = os.getenv("POSTGRE_DATABASE_URL")
pg_engine = create_engine(DATABASE_URL)

# PostgreSQLの設定
PGSession = sessionmaker(bind=pg_engine)

# セッション作成
sqlite_db = SQLiteSession()
pg_db = PGSession()

# 各テーブルを移す
def migrate_model(model_class):
    records = sqlite_db.query(model_class).all()
    for record in records:
        data = record.__dict__.copy()
        data.pop("_sa_instance_state", None)
        # data.pop("id", None)  # IDはAutoIncrementに任せる
        pg_db.add(model_class(**data))
    pg_db.commit()
    print(f"{model_class.__name__} 移行完了（{len(records)} 件）")

def main():
    migrate_model(User)
    migrate_model(Item)
    migrate_model(Coordinate)
    migrate_model(CoordinateItems)

    sqlite_db.close()
    pg_db.close()
    print("✨ 全データ移行完了！")

if __name__ == "__main__":
    main()
