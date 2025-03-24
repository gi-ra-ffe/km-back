"""usersテーブルのカラム名変更 creat_at -> created_at, update_at -> updated_at

Revision ID: 970cec901504
Revises: a2ab6221ec05
Create Date: 2025-03-24 05:19:00.657393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '970cec901504'
down_revision: Union[str, None] = 'a2ab6221ec05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('create_date', new_column_name='created_at')
        batch_op.alter_column('update_at', new_column_name='updated_at')

def downgrade() -> None:
    # カラム名を元に戻す
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('created_at', new_column_name='create_date')
        batch_op.alter_column('updated_at', new_column_name='update_at')