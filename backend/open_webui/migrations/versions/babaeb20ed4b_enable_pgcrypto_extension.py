"""enable_pgcrypto_extension

Revision ID: babaeb20ed4b
Revises: 9f0c9cd09105
Create Date: 2025-06-09 01:40:11.933332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import open_webui.internal.db


# revision identifiers, used by Alembic.
revision: str = 'babaeb20ed4b'
down_revision: Union[str, None] = '9f0c9cd09105'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgcrypto extension
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')


def downgrade() -> None:
    # Drop pgcrypto extension
    op.execute('DROP EXTENSION IF EXISTS pgcrypto;')
