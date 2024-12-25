"""Migration 23_12_2024

Revision ID: 16ddaa28ec30
Revises: 5463ec9e0e72
Create Date: 2024-12-23 22:22:51.099714

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16ddaa28ec30"
down_revision: Union[str, None] = "5463ec9e0e72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "permissions",
        sa.Column(
            "resource",
            sa.Enum(
                "RESTAURANT",
                "MENU_ITEM",
                "ORDER",
                "USER",
                "CATEGORY",
                "PERMISSION",
                "ROLE",
                name="permissionresourceenum",
                native_enum=False,
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "permissions",
        sa.Column(
            "owner",
            sa.Enum("ANY", "OWN", name="permissionownerenum", native_enum=False),
            nullable=False,
        ),
    )
    op.add_column(
        "permissions",
        sa.Column(
            "action",
            sa.Enum(
                "CREATE",
                "READ",
                "UPDATE",
                "DEACTIVATE",
                "DELETE",
                name="permissionactionenum",
                native_enum=False,
            ),
            nullable=False,
        ),
    )
    op.alter_column(
        "permissions",
        "description",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.drop_column("permissions", "slug")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "permissions",
        sa.Column("slug", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.alter_column(
        "permissions",
        "description",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.drop_column("permissions", "action")
    op.drop_column("permissions", "owner")
    op.drop_column("permissions", "resource")
    # ### end Alembic commands ###