"""create interview_sessions table

Revision ID: 23e25d3fb070
Revises: 
Create Date: 2025-12-07 11:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23e25d3fb070'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'interview_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('code_content', sa.Text(), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_sessions_id'), 'interview_sessions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_interview_sessions_id'), table_name='interview_sessions')
    op.drop_table('interview_sessions')
