"""photo_urlのカラム追加

Revision ID: 87204527237d
Revises: 6f915346b3c8
Create Date: 2025-03-31 09:29:03.220914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87204527237d'
down_revision: Union[str, None] = '6f915346b3c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # photo_url カラム追加（items,Coordinate テーブル）
    op.add_column('items', sa.Column('photo_url', sa.String(), nullable=True))
    op.add_column('coordinates', sa.Column('photo_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # カラム削除（items,Coordinate テーブル）
    op.drop_column('items', 'photo_url')
    op.drop_column('coordinates', 'photo_url')
