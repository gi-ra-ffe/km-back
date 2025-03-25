"""user_id を nullable=False に変更

Revision ID: ebcd0699f82e
Revises: 753b04339861
Create Date: 2025-03-25 09:49:47.211279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebcd0699f82e'
down_revision: Union[str, None] = '753b04339861'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("items") as batch_op:
        batch_op.alter_column("user_id", nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("items") as batch_op:
        batch_op.alter_column("user_id", nullable=True)
    # ### end Alembic commands ###
