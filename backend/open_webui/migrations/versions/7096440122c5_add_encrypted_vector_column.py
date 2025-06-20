"""add_encrypted_vector_column

Revision ID: 7096440122c5
Revises: babaeb20ed4b
Create Date: 2025-06-09 14:39:57.893416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import open_webui.internal.db


# revision identifiers, used by Alembic.
revision: str = '7096440122c5'
down_revision: Union[str, None] = 'babaeb20ed4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add encrypted_vector_data column to document_chunk table
    # Note: No index created as encrypted data is too large for PostgreSQL index limits
    op.add_column('document_chunk', sa.Column('encrypted_vector_data', sa.Text(), nullable=True))


def downgrade() -> None:
    # Drop the encrypted_vector_data column (if exists)
    try:
        op.drop_column('document_chunk', 'encrypted_vector_data')
    except Exception:
        pass  # Column might not exist
