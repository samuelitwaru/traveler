"""First migration

Revision ID: 956d60835338
Revises: 
Create Date: 2021-02-17 21:30:56.941274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '956d60835338'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('passenger_name', sa.String(length=128), nullable=False),
    sa.Column('passenger_telephone', sa.String(length=16), nullable=True),
    sa.Column('seat_number', sa.String(length=3), nullable=True),
    sa.Column('pickup', sa.String(length=64), nullable=False),
    sa.Column('stop', sa.String(length=64), nullable=False),
    sa.Column('fare', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('branch_id', sa.Integer(), nullable=False),
    sa.Column('bus_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('grid_id', sa.Integer(), nullable=False),
    sa.Column('pricing_id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ),
    sa.ForeignKeyConstraint(['bus_id'], ['bus.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['grid_id'], ['grid.id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.ForeignKeyConstraint(['pricing_id'], ['pricing.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('branch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=16), nullable=True),
    sa.Column('columns', sa.Integer(), nullable=True),
    sa.Column('rows', sa.Integer(), nullable=True),
    sa.Column('broadcast', sa.Boolean(), nullable=True),
    sa.Column('departure_time', sa.DateTime(), nullable=True),
    sa.Column('schedule_cancelled_reason', sa.String(length=1024), nullable=True),
    sa.Column('booking_deadline', sa.DateTime(), nullable=True),
    sa.Column('free_bus_time', sa.DateTime(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('journey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['journey_id'], ['journey.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('logo', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sid', sa.String(length=64), nullable=False),
    sa.Column('connect_time', sa.DateTime(), nullable=False),
    sa.Column('disconnect_time', sa.DateTime(), nullable=True),
    sa.Column('client_type', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('grid_type', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=3), nullable=True),
    sa.Column('label', sa.String(length=32), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.Column('bus_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.id'], ),
    sa.ForeignKeyConstraint(['bus_id'], ['bus.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_', sa.String(length=64), nullable=True),
    sa.Column('to', sa.String(length=64), nullable=True),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reference', sa.String(length=64), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('app_charge', sa.Integer(), nullable=True),
    sa.Column('method', sa.String(length=64), nullable=True),
    sa.Column('app', sa.String(length=64), nullable=True),
    sa.Column('company_name', sa.String(length=64), nullable=True),
    sa.Column('branch_name', sa.String(length=64), nullable=True),
    sa.Column('bus_number', sa.String(length=16), nullable=True),
    sa.Column('grid_number', sa.String(length=3), nullable=True),
    sa.Column('passenger_name', sa.String(length=64), nullable=True),
    sa.Column('passenger_email', sa.String(length=64), nullable=True),
    sa.Column('passenger_telephone', sa.String(length=16), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('bus_id', sa.Integer(), nullable=True),
    sa.Column('grid_id', sa.Integer(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('journey_id', sa.Integer(), nullable=True),
    sa.Column('pricing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bus_id'], ['bus.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['grid_id'], ['grid.id'], ),
    sa.ForeignKeyConstraint(['journey_id'], ['journey.id'], ),
    sa.ForeignKeyConstraint(['pricing_id'], ['pricing.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pickup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('journey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['journey_id'], ['journey.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pricing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stop', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('journey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['journey_id'], ['journey.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('telephone', sa.String(length=16), nullable=False),
    sa.Column('email_valid', sa.Boolean(), nullable=True),
    sa.Column('telephone_valid', sa.Boolean(), nullable=True),
    sa.Column('credit', sa.Float(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_manager', sa.Boolean(), nullable=True),
    sa.Column('is_cashier', sa.Boolean(), nullable=True),
    sa.Column('is_passenger', sa.Boolean(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.Column('expiry', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('recovery_password', sa.String(length=128), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('token')
    op.drop_table('status')
    op.drop_table('profile')
    op.drop_table('pricing')
    op.drop_table('pickup')
    op.drop_table('payment')
    op.drop_table('journey')
    op.drop_table('grid')
    op.drop_table('connection')
    op.drop_table('company')
    op.drop_table('bus')
    op.drop_table('branch')
    op.drop_table('booking')
    # ### end Alembic commands ###
