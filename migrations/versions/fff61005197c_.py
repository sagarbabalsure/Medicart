"""empty message

Revision ID: fff61005197c
Revises: 
Create Date: 2020-07-15 23:18:31.824564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fff61005197c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyer_register',
    sa.Column('Buyer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('mobile_no', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('mode', sa.String(length=50), nullable=True),
    sa.Column('about_me', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('Buyer_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile_no'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cart',
    sa.Column('cart_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('cart_id')
    )
    op.create_table('confirmed_order',
    sa.Column('order_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('Quantity', sa.Integer(), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('seller_register',
    sa.Column('Seller_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('mobile_no', sa.String(length=50), nullable=True),
    sa.Column('company_name', sa.String(length=50), nullable=True),
    sa.Column('mode', sa.String(length=50), nullable=True),
    sa.Column('about_me', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('Seller_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile_no'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('username')
    )
    op.create_table('items',
    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('medicine_name', sa.String(length=100), nullable=False),
    sa.Column('manufacturer', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('composition', sa.String(length=200), nullable=True),
    sa.Column('precaution', sa.String(length=200), nullable=True),
    sa.Column('Seller_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Seller_id'], ['seller_register.Seller_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('seller_register')
    op.drop_table('confirmed_order')
    op.drop_table('cart')
    op.drop_table('buyer_register')
    # ### end Alembic commands ###