"""SQLAlchemy Models for Investment Platform"""

from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, Text, Enum, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

Base = declarative_base()

# ============================================================
# Core Investment Models
# ============================================================

class Investment(Base):
    """Investment opportunity record"""
    __tablename__ = "investments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    sector = Column(String(100))
    region = Column(String(100))
    country = Column(String(100))
    investment_type = Column(String(50))  # equity, debt, real_estate, alternatives
    status = Column(String(50), default="draft")  # draft, active, closed, withdrawn
    
    # Financial metrics
    target_amount = Column(Float)  # in millions
    minimum_check_size = Column(Float)
    valuation = Column(Float)
    projected_irr = Column(Float)
    projected_moic = Column(Float)
    time_horizon = Column(String(50))  # short, medium, long
    
    # Risk factors
    risk_score = Column(Float, default=0.0)  # 0-100
    liquidity_score = Column(Float, default=0.0)
    geopolitical_exposure = Column(Float, default=0.0)
    esg_score = Column(Float, default=0.0)
    
    # Overall scoring
    overall_score = Column(Float, default=0.0)
    recommendation = Column(String(50))  # buy, hold, sell, investigate
    
    # Metadata
    source = Column(String(100))  # internal_team, research_feed, broker, api
    data_encrypted = Column(Boolean, default=True)
    pii_present = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    updated_by = Column(String(100))
    
    # Relationships
    portfolios = relationship("Portfolio", secondary="portfolio_investments")
    documents = relationship("ResearchDocument")
    scores = relationship("InvestmentScore")
    briefs = relationship("InvestmentBrief")
    
    __table_args__ = (
        Index("idx_inv_status_created", "status", "created_at"),
        Index("idx_inv_sector_region", "sector", "region"),
    )

class Portfolio(Base):
    """Portfolio of investments"""
    __tablename__ = "portfolios"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    status = Column(String(50), default="active")
    
    # Portfolio metrics
    total_value = Column(Float, default=0.0)
    total_invested = Column(Float, default=0.0)
    current_value = Column(Float, default=0.0)
    realized_returns = Column(Float, default=0.0)
    unrealized_returns = Column(Float, default=0.0)
    
    # Risk metrics
    portfolio_volatility = Column(Float, default=0.0)
    portfolio_beta = Column(Float, default=1.0)
    var_95 = Column(Float)  # Value at Risk (95%)
    
    # Allocation
    sector_allocation = Column(JSON)  # {sector: weight}
    region_allocation = Column(JSON)  # {region: weight}
    asset_type_allocation = Column(JSON)  # {type: weight}
    
    # Metadata
    owner_id = Column(String(100), index=True)
    owner_email = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    investments = relationship("Investment", secondary="portfolio_investments")
    transactions = relationship("Transaction")
    analytics = relationship("PortfolioAnalytic")
    
    __table_args__ = (
        Index("idx_port_owner_status", "owner_id", "status"),
    )

class PortfolioInvestment(Base):
    """Join table for portfolio-investment many-to-many"""
    __tablename__ = "portfolio_investments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False)
    investment_id = Column(String(36), ForeignKey("investments.id"), nullable=False)
    
    # Allocation in this portfolio
    weight = Column(Float)  # 0-100 (percentage)
    amount_invested = Column(Float)
    units_held = Column(Float)
    cost_basis = Column(Float)
    current_value = Column(Float)
    
    # Trade info
    entry_date = Column(DateTime)
    purchase_price = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(Base):
    """Individual transactions (buys, sells, distributions)"""
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False, index=True)
    investment_id = Column(String(36), ForeignKey("investments.id"), nullable=False)
    
    transaction_type = Column(String(50))  # buy, sell, dividend, distribution, fee
    quantity = Column(Float)
    price = Column(Float)
    amount = Column(Float)
    currency = Column(String(10), default="USD")
    
    transaction_date = Column(DateTime, nullable=False, index=True)
    settlement_date = Column(DateTime)
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_trans_portfolio_date", "portfolio_id", "transaction_date"),
    )

class MarketData(Base):
    """Historical market data for analysis"""
    __tablename__ = "market_data"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String(100), nullable=False, index=True)
    asset_type = Column(String(50))  # stock, index, commodity, forex
    
    data_date = Column(DateTime, nullable=False, index=True)
    
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    
    returns = Column(Float)
    volatility = Column(Float)
    
    source = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_market_asset_date", "asset_id", "data_date"),
    )

# ============================================================
# Research & Document Models
# ============================================================

class ResearchDocument(Base):
    """Research documents and reports"""
    __tablename__ = "research_documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investment_id = Column(String(36), ForeignKey("investments.id"), index=True)
    
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text)
    document_type = Column(String(50))  # research_report, market_analysis, news, email
    
    # Document metadata
    source_url = Column(String(500))
    author = Column(String(255))
    publish_date = Column(DateTime)
    
    # Analysis results (populated by agents)
    summary = Column(Text)
    key_insights = Column(JSON)  # List of insights
    risk_flags = Column(JSON)  # List of risk flags
    sentiment = Column(String(50))  # positive, negative, neutral
    strategy_signals = Column(JSON)  # List of signals
    confidence_score = Column(Float, default=0.0)
    
    # Embeddings for RAG
    embedding_id = Column(String(100))  # Reference to Qdrant vector ID
    embedding_collection = Column(String(100))  # Which Qdrant collection
    
    # Status
    processed = Column(Boolean, default=False)
    indexed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_doc_investment_type", "investment_id", "document_type"),
    )

class EntityExtraction(Base):
    """Extracted entities from documents"""
    __tablename__ = "entity_extractions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("research_documents.id"), index=True)
    
    entity_type = Column(String(50))  # company, person, location, sector, kpi
    entity_value = Column(String(500), index=True)
    confidence_score = Column(Float)
    
    # Context
    context = Column(Text)  # Surrounding text
    
    created_at = Column(DateTime, default=datetime.utcnow)

# ============================================================
# Risk & Monitoring Models
# ============================================================

class RiskEvent(Base):
    """Risk events and alerts"""
    __tablename__ = "risk_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), index=True)
    investment_id = Column(String(36), ForeignKey("investments.id"), index=True)
    
    event_type = Column(String(50))  # drawdown, volatility_spike, fx_shock, liquidity_event
    severity = Column(String(20))  # low, medium, high, critical
    
    description = Column(Text)
    impact_estimate = Column(Float)
    
    # Context
    triggered_at = Column(DateTime, nullable=False, index=True)
    resolved_at = Column(DateTime)
    
    recommended_action = Column(Text)
    status = Column(String(50), default="active")  # active, acknowledged, resolved
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_risk_portfolio_status", "portfolio_id", "status"),
    )

# ============================================================
# Scoring & Analytics Models
# ============================================================

class InvestmentScore(Base):
    """Investment opportunity scores"""
    __tablename__ = "investment_scores"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investment_id = Column(String(36), ForeignKey("investments.id"), index=True, nullable=False)
    
    overall_score = Column(Float, nullable=False)  # 0-100
    recommendation = Column(String(50))  # buy, hold, sell, investigate
    
    # Score breakdown
    risk_score = Column(Float)
    return_score = Column(Float)
    liquidity_score = Column(Float)
    geopolitical_score = Column(Float)
    esg_score = Column(Float)
    
    # Score drivers (JSON format)
    score_drivers = Column(JSON)  # List of {factor, contribution, direction}
    
    # Next actions
    next_actions = Column(JSON)  # List of recommended actions
    
    # Metadata
    model_version = Column(String(50))
    scored_by = Column(String(100))  # API, agent, manual
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PortfolioAnalytic(Base):
    """Portfolio analysis results"""
    __tablename__ = "portfolio_analytics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), index=True, nullable=False)
    
    analysis_date = Column(DateTime, nullable=False, index=True)
    analysis_type = Column(String(50))  # forecast, stress_test, scenario_analysis
    
    # Results
    results = Column(JSON)  # Flexible structure for different analysis types
    
    # Forecasts
    forecast_returns = Column(JSON)  # {period: expected_return}
    forecast_volatility = Column(JSON)  # {period: volatility}
    
    # Stress test results
    stress_scenarios = Column(JSON)  # {scenario_name: portfolio_impact}
    
    # Recommendations
    recommendations = Column(JSON)  # List of recommendations
    
    created_at = Column(DateTime, default=datetime.utcnow)

class InvestmentBrief(Base):
    """Generated investment briefs (dossiers)"""
    __tablename__ = "investment_briefs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investment_id = Column(String(36), ForeignKey("investments.id"), index=True, nullable=False)
    
    brief_content = Column(JSON)  # {executive_summary, risk_analysis, ...}
    pdf_url = Column(String(500))  # S3 URL to PDF version
    
    # Metadata
    generated_by = Column(String(100))  # Agent name
    generated_at = Column(DateTime, nullable=False, index=True)
    
    # Status
    status = Column(String(50), default="draft")  # draft, approved, published
    approved_by = Column(String(100))
    approved_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ============================================================
# Compliance & Governance Models
# ============================================================

class AuditLog(Base):
    """Append-only audit logs for compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Who performed the action
    user_id = Column(String(100), nullable=False, index=True)
    user_email = Column(String(255))
    
    # What action
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50))  # investment, portfolio, document, etc
    resource_id = Column(String(100), index=True)
    
    # Details
    details = Column(JSON)  # Action-specific details
    
    # Status
    status = Column(String(50))  # success, failure
    error_message = Column(Text)
    
    # Metadata
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index("idx_audit_user_action", "user_id", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
    )

class Consent(Base):
    """PDPL consent records"""
    __tablename__ = "consents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Who gave consent
    user_id = Column(String(100), nullable=False, index=True)
    user_email = Column(String(255), nullable=False)
    
    # What data types
    data_type = Column(String(50), nullable=False)  # personal_data, trading_data, market_data
    
    # Purpose
    purpose = Column(String(255), nullable=False)  # analysis, reporting, research
    
    # Scope
    scope = Column(String(50))  # own_data, all_data
    
    # Validity
    given_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime)
    revoked_at = Column(DateTime)
    
    # Status
    status = Column(String(50), default="active")  # active, revoked, expired
    
    # Reference
    terms_version = Column(String(50))
    ip_address = Column(String(50))
    
    __table_args__ = (
        Index("idx_consent_user_status", "user_id", "status"),
    )

class DataEncryption(Base):
    """Encryption key references and PII encryption markers"""
    __tablename__ = "data_encryption"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    resource_type = Column(String(50))  # investment, portfolio, document
    resource_id = Column(String(100), nullable=False, index=True)
    
    field_name = Column(String(100))  # Which field is encrypted
    is_pii = Column(Boolean, default=True)  # Is this PII?
    
    key_id = Column(String(100))  # pgcrypto key reference
    encryption_algorithm = Column(String(50))  # aes-256, etc
    
    encrypted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # For data minimization
