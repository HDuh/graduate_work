"""do migrations

Revision ID: 3789690e2115
Revises: 
Create Date: 2022-12-16 20:30:43.640540

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql as pg

# revision identifiers, used by Alembic.
revision = '3789690e2115'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('customer_id'),
    )

    op.create_table(
        'order',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=255), nullable=False),

        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'product',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('product_type', sa.String(length=255), nullable=False),
        sa.Column('product_stripe_id', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255)),
        sa.Column('duration', sa.Integer()),
        sa.Column('price', sa.Float()),
        sa.Column('currency_code', sa.String(length=3)),
        sa.Column('recurring', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'subscription',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['product.id']),

    )

    op.create_table('order_product',
    sa.Column('order_id', pg.UUID(as_uuid=True), nullable=True),
    sa.Column('product_id', pg.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id']),
    )


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('order')
    op.drop_table('product')
    op.drop_table('order_product')
    op.drop_table('subscription')
