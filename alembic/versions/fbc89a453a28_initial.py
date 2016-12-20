"""initial

Revision ID: fbc89a453a28
Revises:
Create Date: 2016-12-20 15:07:21.118877

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fbc89a453a28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('task',
                    sa.Column('uuid', postgresql.UUID(), server_default=sa.text(u'uuid_generate_v1mc()'), nullable=False),
                    sa.Column('sub_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('upd_date', sa.DateTime(), nullable=True),
                    sa.Column('status', sa.Integer(), server_default='0', nullable=True),
                    sa.Column('dst_url', sa.String(length=2083), nullable=True),
                    sa.Column('src_url', sa.String(length=2083), nullable=False),
                    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade():
    op.drop_table('task')
