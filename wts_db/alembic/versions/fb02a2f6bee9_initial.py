"""Initial

Revision ID: fb02a2f6bee9
Revises: 
Create Date: 2016-12-27 16:19:14.191138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fb02a2f6bee9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('uuid', postgresql.UUID(), server_default=sa.text(u'uuid_generate_v1mc()'), nullable=False),
    sa.Column('sub_date', sa.DateTime(), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dst_url', sa.String(length=2083), nullable=True),
    sa.Column('src_url', sa.String(length=2083), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###
