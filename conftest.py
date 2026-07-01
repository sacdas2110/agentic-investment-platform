"""Pytest configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
from unittest.mock import Mock, patch

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    from services.shared.models import Base
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_session(test_db):
    """Create test session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    with patch('redis.from_url') as mock:
        mock.return_value = Mock(spec=redis.Redis)
        yield mock

@pytest.fixture
def mock_kafka():
    """Mock Kafka producer"""
    with patch('kafka.KafkaProducer') as mock:
        mock.return_value.send.return_value.get.return_value = Mock(
            topic='test',
            partition=0,
            offset=0
        )
        yield mock

@pytest.fixture
def sample_investment():
    """Sample investment for testing"""
    return {
        "name": "Tech Startup Fund",
        "description": "Early stage tech investments",
        "sector": "Technology",
        "region": "Middle East",
        "country": "AE",
        "investment_type": "equity",
        "target_amount": 10.0,
        "minimum_check_size": 0.5,
        "valuation": 50.0,
        "projected_irr": 0.35,
        "projected_moic": 3.5,
        "time_horizon": "medium",
        "risk_score": 65.0,
        "liquidity_score": 30.0,
    }

@pytest.fixture
def sample_portfolio():
    """Sample portfolio for testing"""
    return {
        "name": "Growth Portfolio",
        "description": "High-growth investment portfolio",
        "status": "active",
        "owner_email": "investor@example.com",
    }

@pytest.fixture
def sample_document():
    """Sample document for testing"""
    return {
        "title": "Investment Market Analysis 2024",
        "content": "Market analysis for tech sector investments in Dubai",
        "document_type": "research_report",
        "source_url": "https://example.com/report.pdf",
        "author": "Research Team",
    }

# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
