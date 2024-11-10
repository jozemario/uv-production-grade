"""fix_relationships

Revision ID: 38e4bf0477a5
Revises: 71139a54084d
Create Date: 2024-10-25 12:43:02.982269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e4bf0477a5'
down_revision = '71139a54084d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.UUID(),
               type_=sa.String(length=320),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.String(length=320),
               type_=sa.UUID(),
               existing_nullable=False)
    # ### end Alembic commands ###