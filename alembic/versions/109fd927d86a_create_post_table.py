"""create post table

Revision ID: 109fd927d86a
Revises: 
Create Date: 2025-05-03 22:23:15.601141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '109fd927d86a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.INTEGER,nullable=False,primary_key=True),
    sa.Column('title',sa.String,nullable=False) )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass