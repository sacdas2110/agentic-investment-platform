"""Initial migration - Create all base tables"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create investments table
    op.create_table(
        'investments',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('sector', sa.String(100)),
        sa.Column('region', sa.String(100)),
        sa.Column('country', sa.String(100)),
        sa.Column('investment_type', sa.String(50)),
        sa.Column('status', sa.String(50), server_default='draft'),
        sa.Column('target_amount', sa.Float()),
        sa.Column('minimum_check_size', sa.Float()),
        sa.Column('valuation', sa.Float()),
        sa.Column('projected_irr', sa.Float()),
        sa.Column('projected_moic', sa.Float()),
        sa.Column('time_horizon', sa.String(50)),
        sa.Column('risk_score', sa.Float(), server_default='0.0'),
        sa.Column('liquidity_score', sa.Float(), server_default='0.0'),
        sa.Column('geopolitical_exposure', sa.Float(), server_default='0.0'),
        sa.Column('esg_score', sa.Float(), server_default='0.0'),
        sa.Column('overall_score', sa.Float(), server_default='0.0'),
        sa.Column('recommendation', sa.String(50)),
        sa.Column('source', sa.String(100)),
        sa.Column('data_encrypted', sa.Boolean(), server_default='true'),
        sa.Column('pii_present', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_investments_name', 'name'),
        sa.Index('idx_investments_status_created', 'status', 'created_at'),
        sa.Index('idx_investments_sector_region', 'sector', 'region'),
    )
    
    # Create portfolios table
    op.create_table(
        'portfolios',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(50), server_default='active'),
        sa.Column('total_value', sa.Float(), server_default='0.0'),
        sa.Column('total_invested', sa.Float(), server_default='0.0'),
        sa.Column('current_value', sa.Float(), server_default='0.0'),
        sa.Column('realized_returns', sa.Float(), server_default='0.0'),
        sa.Column('unrealized_returns', sa.Float(), server_default='0.0'),
        sa.Column('portfolio_volatility', sa.Float(), server_default='0.0'),
        sa.Column('portfolio_beta', sa.Float(), server_default='1.0'),
        sa.Column('var_95', sa.Float()),
        sa.Column('sector_allocation', postgresql.JSON()),
        sa.Column('region_allocation', postgresql.JSON()),
        sa.Column('asset_type_allocation', postgresql.JSON()),
        sa.Column('owner_id', sa.String(100)),
        sa.Column('owner_email', sa.String(255)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_portfolios_name', 'name'),
        sa.Index('idx_portfolios_owner_status', 'owner_id', 'status'),
    )
    
    # Create research_documents table
    op.create_table(
        'research_documents',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('investment_id', sa.String(36), sa.ForeignKey('investments.id')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('document_type', sa.String(50)),
        sa.Column('source_url', sa.String(500)),
        sa.Column('author', sa.String(255)),
        sa.Column('publish_date', sa.DateTime()),
        sa.Column('summary', sa.Text()),
        sa.Column('key_insights', postgresql.JSON()),
        sa.Column('risk_flags', postgresql.JSON()),
        sa.Column('sentiment', sa.String(50)),
        sa.Column('strategy_signals', postgresql.JSON()),
        sa.Column('confidence_score', sa.Float(), server_default='0.0'),
        sa.Column('embedding_id', sa.String(100)),
        sa.Column('embedding_collection', sa.String(100)),
        sa.Column('processed', sa.Boolean(), server_default='false'),
        sa.Column('indexed', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_documents_title', 'title'),
        sa.Index('idx_documents_investment_type', 'investment_id', 'document_type'),
    )
    
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=False),
        sa.Column('user_email', sa.String(255)),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50)),
        sa.Column('resource_id', sa.String(100)),
        sa.Column('details', postgresql.JSON()),
        sa.Column('status', sa.String(50)),
        sa.Column('error_message', sa.Text()),
        sa.Column('ip_address', sa.String(50)),
        sa.Column('user_agent', sa.String(500)),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_audit_user_action', 'user_id', 'action'),
        sa.Index('idx_audit_resource', 'resource_type', 'resource_id'),
        sa.Index('idx_audit_timestamp', 'timestamp'),
    )
    
    # Create consents table (PDPL compliance)
    op.create_table(
        'consents',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=False),
        sa.Column('user_email', sa.String(255), nullable=False),
        sa.Column('data_type', sa.String(50), nullable=False),
        sa.Column('purpose', sa.String(255), nullable=False),
        sa.Column('scope', sa.String(50)),
        sa.Column('given_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime()),
        sa.Column('revoked_at', sa.DateTime()),
        sa.Column('status', sa.String(50), server_default='active'),
        sa.Column('terms_version', sa.String(50)),
        sa.Column('ip_address', sa.String(50)),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_consents_user_status', 'user_id', 'status'),
    )

def downgrade():
    op.drop_table('consents')
    op.drop_table('audit_logs')
    op.drop_table('research_documents')
    op.drop_table('portfolios')
    op.drop_table('investments')
