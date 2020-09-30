"""empty message

Revision ID: 0d7b5e00814d
Revises: bee4527759b3
Create Date: 2020-09-30 08:20:45.782832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d7b5e00814d'
down_revision = 'bee4527759b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('localidad',
    sa.Column('localidad_id', sa.Integer(), nullable=False),
    sa.Column('descripcion', sa.String(length=80), nullable=False),
    sa.Column('provincia_id', sa.Integer(), nullable=False),
    sa.Column('ts_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['provincia_id'], ['provincia.provincia_id'], ),
    sa.PrimaryKeyConstraint('localidad_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('localidad')
    # ### end Alembic commands ###