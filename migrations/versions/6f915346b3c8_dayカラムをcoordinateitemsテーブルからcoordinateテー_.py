"""dayカラムをCoordinateItemsテーブルからCoordinateテーブルに移動

Revision ID: 6f915346b3c8
Revises: ebcd0699f82e
Create Date: 2025-03-30 04:19:56.925092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f915346b3c8'
down_revision: Union[str, None] = 'ebcd0699f82e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. day カラム追加（Coordinate テーブル）
    op.add_column('coordinates', sa.Column('day', sa.String(), nullable=True))

    # 2. 中間テーブルからコピー（手動 or SQL）
    op.execute("""
        UPDATE coordinates
        SET day = (
            SELECT day FROM coordinate_items
            WHERE coordinate_items.coordinate_id = coordinates.id
            LIMIT 1
        )
    """)

    # 3. 中間テーブルの day カラム削除
    op.drop_column('coordinate_items', 'day')

    pass


def downgrade() -> None:
    """Downgrade schema."""
    # 1. coordinate_items に day カラムを復元
    op.add_column('coordinate_items', sa.Column('day', sa.String(), nullable=True))

    # 2. coordinates から day を coordinate_items に戻す（同じく1件だけ）
    op.execute("""
        UPDATE coordinate_items
        SET day = (
            SELECT c.day
            FROM coordinates c
            WHERE c.id = coordinate_items.coordinate_id
        )
    """)

    # 3. coordinates から day カラム削除
    op.drop_column('coordinates', 'day')
    pass
