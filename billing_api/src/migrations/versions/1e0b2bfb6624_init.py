"""init

Revision ID: 1e0b2bfb6624
Revises: 
Create Date: 2022-12-24 14:49:56.908602

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1e0b2bfb6624'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('customer_id', sa.String(length=128), nullable=False),
    sa.Column('price_id', sa.String(length=128), nullable=True),
    sa.Column('status', sa.Enum('UNPAID', 'PAID', 'ERROR', 'CANCELED', name='paymentstate'), nullable=False),
    sa.Column('service_name', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    # ### end Alembic commands ###
