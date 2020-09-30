"""empty message

Revision ID: e5a842bfaa6c
Revises: 0d7b5e00814d
Create Date: 2020-09-30 08:42:26.520592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a842bfaa6c'
down_revision = '0d7b5e00814d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domicilio',
    sa.Column('domicilio_id', sa.Integer(), nullable=False),
    sa.Column('calle', sa.String(length=50), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=True),
    sa.Column('departamento', sa.String(length=50), nullable=True),
    sa.Column('piso', sa.Integer(), nullable=True),
    sa.Column('aclaracion', sa.String(length=80), nullable=False),
    sa.Column('localidad_id', sa.Integer(), nullable=False),
    sa.Column('ts_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['localidad_id'], ['localidad.localidad_id'], ),
    sa.PrimaryKeyConstraint('domicilio_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('domicilio')
    # ### end Alembic commands ###
