"""Shared utilities for all microservices"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import redis
from kafka import KafkaProducer

logger = logging.getLogger(__name__)

# ============================================================
# Logging Configuration
# ============================================================

def setup_logging(service_name: str, log_level: str = "INFO"):
    """Configure structured JSON logging"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(service_name)
    return logger

# ============================================================
# Event Publishing
# ============================================================

class EventPublisher:
    """Kafka event publisher with error handling"""
    
    def __init__(self, bootstrap_servers: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas
            retries=3,
            compression_type='gzip'
        )
    
    def publish_event(
        self,
        topic: str,
        event_type: str,
        payload: Dict[str, Any],
        priority: str = "medium",
        correlation_id: Optional[str] = None
    ) -> str:
        """Publish event to Kafka"""
        event_id = str(uuid.uuid4())
        
        event = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_service": "service-name",  # Override in subclass
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "priority": priority,
            "payload": payload,
            "metadata": {}
        }
        
        try:
            future = self.producer.send(topic, event)
            record_metadata = future.get(timeout=10)
            logger.info(f"Event published: {event_id} -> {topic}")
            return event_id
        except Exception as e:
            logger.error(f"Failed to publish event: {str(e)}")
            raise
    
    def close(self):
        """Close producer connection"""
        self.producer.flush()
        self.producer.close()

# ============================================================
# Caching Utilities
# ============================================================

class CacheManager:
    """Redis cache wrapper with TTL support"""
    
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error: {str(e)}")
            return None
    
    def set(
        self,
        key: str,
        value: Dict[str, Any],
        ttl_seconds: int = 3600
    ) -> bool:
        """Set value in cache with TTL"""
        try:
            self.redis_client.setex(
                key,
                ttl_seconds,
                json.dumps(value)
            )
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {str(e)}")
            return False
    
    def clear(self, pattern: str = "*") -> int:
        """Clear keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Cache clear error: {str(e)}")
            return 0

# ============================================================
# Rate Limiting
# ============================================================

class RateLimiter:
    """Redis-based rate limiting"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    def is_allowed(
        self,
        key: str,
        max_requests: int = 100,
        window_seconds: int = 60
    ) -> bool:
        """Check if request is allowed"""
        current = self.redis_client.get(key)
        
        if current is None:
            self.redis_client.setex(key, window_seconds, 1)
            return True
        
        current_count = int(current)
        if current_count < max_requests:
            self.redis_client.incr(key)
            return True
        
        return False
    
    def get_remaining(
        self,
        key: str,
        max_requests: int = 100
    ) -> int:
        """Get remaining requests in window"""
        current = self.redis_client.get(key)
        if current is None:
            return max_requests
        return max(0, max_requests - int(current))

# ============================================================
# Data Validation
# ============================================================

def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_uuid(value: str) -> bool:
    """Validate UUID format"""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

def sanitize_input(input_str: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    return input_str.strip()[:max_length]

# ============================================================
# Pagination
# ============================================================

class PaginationParams:
    """Pagination helper"""
    
    def __init__(self, page: int = 1, page_size: int = 20):
        self.page = max(1, page)
        self.page_size = min(max(1, page_size), 100)  # Max 100
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size
    
    def paginate_query(self, query):
        """Apply pagination to SQLAlchemy query"""
        return query.offset(self.offset).limit(self.limit)

# ============================================================
# Response Formatting
# ============================================================

def create_response(
    status: str,
    data: Any = None,
    message: Optional[str] = None,
    errors: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Standard response format"""
    response = {
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    if errors:
        response["errors"] = errors
    
    return response

def create_error_response(
    error_code: str,
    message: str,
    status_code: int = 400
) -> Dict[str, Any]:
    """Standard error response"""
    return {
        "status": "error",
        "error_code": error_code,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# ============================================================
# Retry Logic
# ============================================================

import asyncio
from functools import wraps

def retry(
    max_attempts: int = 3,
    backoff_seconds: float = 1.0,
    backoff_multiplier: float = 2.0
):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    wait_time = backoff_seconds * (backoff_multiplier ** (attempt - 1))
                    logger.warning(
                        f"Attempt {attempt} failed. Retrying in {wait_time}s: {str(e)}"
                    )
                    await asyncio.sleep(wait_time)
        
        return async_wrapper
    return decorator
