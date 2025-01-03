"""Migration 21_12_2024

Revision ID: b30c01167f54
Revises: 64c9bd259c71
Create Date: 2024-12-21 11:56:16.268099

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b30c01167f54"
down_revision: Union[str, None] = "64c9bd259c71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("password", sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "password")
    # ### end Alembic commands ###
