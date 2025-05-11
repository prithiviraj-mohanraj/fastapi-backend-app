"""add content column to post table

Revision ID: 462f3987e81c
Revises: 109fd927d86a
Create Date: 2025-05-03 22:26:25.129296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '462f3987e81c'
down_revision: Union[str, None] = '109fd927d86a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass