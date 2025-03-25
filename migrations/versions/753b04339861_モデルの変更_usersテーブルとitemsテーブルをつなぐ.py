"""モデルの変更：UsersテーブルとItemsテーブルをつなぐ

Revision ID: 753b04339861
Revises: 970cec901504
Create Date: 2025-03-25 07:53:20.624584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '753b04339861'
down_revision: Union[str, None] = '970cec901504'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('items') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_items_user_id', 'users', ['user_id'], ['id'])
        batch_op.drop_index('ix_items_category')
        batch_op.create_index(op.f('ix_items_category'), ['category'], unique=False)

def downgrade() -> None:
    with op.batch_alter_table('items') as batch_op:
        batch_op.drop_constraint('fk_items_user_id', type_='foreignkey')
        batch_op.drop_index(op.f('ix_items_category'))
        batch_op.create_index('ix_items_category', ['category'], unique=True)
        batch_op.drop_column('user_id')
