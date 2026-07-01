"""Kafka event schemas and producer/consumer utilities"""

from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json

# ============================================================
# Event Types
# ============================================================

class EventType(str, Enum):
    """Event types flowing through Kafka"""
    INVESTMENT_INGESTED = "investment.ingested"
    DOCUMENT_ANALYZED = "document.analyzed"
    RESEARCH_GENERATED = "research.generated"
    INVESTMENT_SCORED = "investment.scored"
    PORTFOLIO_ANALYZED = "portfolio.analyzed"
    RISK_DETECTED = "risk.detected"
    BRIEFING_GENERATED = "briefing.generated"
    MARKET_DATA_RECEIVED = "market_data.received"

class EventPriority(str, Enum):
    """Event priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# ============================================================
# Base Event Schema
# ============================================================

class BaseEvent(BaseModel):
    """Base event schema for all events"""
    event_id: str
    event_type: EventType
    timestamp: datetime
    source_service: str
    correlation_id: str  # For tracing across services
    priority: EventPriority = EventPriority.MEDIUM
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = {}

# ============================================================
# Specific Event Schemas
# ============================================================

class InvestmentIngestedEvent(BaseEvent):
    """Event: Investment document ingested"""
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "investment.ingested",
                "payload": {
                    "document_id": "doc-123",
                    "file_name": "investment_report.pdf",
                    "document_type": "research",
                    "file_size": 1024000,
                    "entities_extracted": ["Company A", "Tech Sector", "US"]
                }
            }
        }

class DocumentAnalyzedEvent(BaseEvent):
    """Event: Document analyzed by intelligence agent"""
    pass

class ResearchGeneratedEvent(BaseEvent):
    """Event: Research synthesis complete"""
    pass

class InvestmentScoredEvent(BaseEvent):
    """Event: Investment scored"""
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "investment.scored",
                "payload": {
                    "investment_id": "inv-123",
                    "score": 75.5,
                    "recommendation": "buy"
                }
            }
        }

class PortfolioAnalyzedEvent(BaseEvent):
    """Event: Portfolio analysis complete"""
    pass

class RiskDetectedEvent(BaseEvent):
    """Event: Risk event detected"""
    pass

class BriefingGeneratedEvent(BaseEvent):
    """Event: Investment brief generated"""
    pass

class MarketDataReceivedEvent(BaseEvent):
    """Event: Market data received for processing"""
    pass

# ============================================================
# Kafka Topics
# ============================================================

KAFKA_TOPICS = {
    "investment-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 604800000,  # 7 days
    },
    "document-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 604800000,
    },
    "research-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 604800000,
    },
    "scoring-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 604800000,
    },
    "analytics-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 604800000,
    },
    "risk-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 2592000000,  # 30 days for risk history
    },
    "briefing-events": {
        "partitions": 3,
        "replication_factor": 2,
        "retention_ms": 604800000,
    },
    "market-data-events": {
        "partitions": 5,  # Higher partitions for high-volume market data
        "replication_factor": 2,
        "retention_ms": 2592000000,  # 30 days
    },
}
