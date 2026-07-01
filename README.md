# Agentic Investment Intelligence Platform

[![CI/CD Pipeline](https://github.com/sacdas2110/agentic-investment-platform/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/sacdas2110/agentic-investment-platform/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-ready-blueviolet.svg)](https://kubernetes.io/)

## 🚀 Vision

> **Every inbound investment query, document, dataset, or research request should be processed, analysed, summarised, and routed by specialised AI agents within seconds — producing actionable intelligence, risk insights, and investment briefs with zero analyst intervention.**

## 📋 Table of Contents

- [Core Features](#-core-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Service Overview](#-service-overview)
- [Data Flow](#-data-flow)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Compliance](#-compliance)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Core Features

### 🤖 Intelligent Agent System
- **8 Specialized AI Agents** orchestrated via Kafka
- Real-time document processing and analysis
- Multi-model inference (HuggingFace, XGBoost, Prophet, Local LLM)
- Event-driven architecture with guaranteed delivery

### 📊 Investment Analysis
- Automated investment opportunity scoring (0-100)
- Risk assessment and monitoring
- Portfolio analytics and forecasting
- Comparable deal analysis
- Market trend synthesis

### 🔍 Advanced RAG (Retrieval-Augmented Generation)
- Semantic search across investment documents
- Cross-reference internal + external datasets
- Investment thesis generation
- Market context awareness (GCC/Dubai focus)

### 📈 Analytics & Visualization
- Real-time dashboards
- Portfolio performance tracking
- Risk heatmaps
- Scenario analysis (Base/Upside/Downside)
- Monte Carlo simulations

### 🔐 Enterprise Security & Compliance
- PDPL (Personal Data Protection Law) compliance
- Append-only audit logs (7-year retention)
- PII encryption at rest (pgcrypto)
- RBAC via Keycloak
- Cross-border transfer controls

### 📱 Analyst Portal
- Next.js-based SPA
- Keycloak SSO integration
- Document upload & management
- Investment pipeline viewer
- Real-time alerts

## 🏗️ Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────┐
│           Analyst Portal (Next.js)                  │
│           http://localhost:3000                     │
└─────────────────────────────────────────┬───────────┘
                                          │
                    ┌─────────────────────▼──────────────────────┐
                    │    API Gateway (FastAPI)                   │
                    │    http://localhost:8000                   │
                    │    - Auth validation                       │
                    │    - Rate limiting                         │
                    │    - Request routing                       │
                    └──────────────┬───────────────────────────┬─┘
                                   │                           │
        ┌──────────────────────────┼───────────────────┬──────┴─────┐
        │                          │                   │            │
        ▼                          ▼                   ▼            ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐
  │Ingestion     │ │Document      │ │Research     │ │Scorer    │
  │Agent (8001)  │ │Intel (8002)  │ │RAG (8003)   │ │(8004)    │
  └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘
        │                  │                  │            │
        └──────────────────┼──────────────────┼────────────┘
                           │
                ┌──────────▼──────────┐
                │  Kafka Event Bus    │
                │  (9092)             │
                │  - 8 core topics    │
                │  - Event brokers    │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┬────────────────┐
        │                  │                  │                │
        ▼                  ▼                  ▼                ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐
  │Portfolio     │ │Risk Monitor  │ │Briefing      │ │Compliance│
  │Analytics     │ │(8006)        │ │Gen (8007)    │ │(8008)    │
  │(8005)        │ │              │ │              │ │          │
  └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘

  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
  │PostgreSQL      │ │Qdrant (6333)   │ │Redis (6379)    │
  │(5432)          │ │- Embeddings    │ │- Cache         │
  │- Investments   │ │- RAG search    │ │- Sessions      │
  │- Portfolios    │ │                │ │- Rate limits   │
  │- Audit logs    │ └────────────────┘ └────────────────┘
  │- PDPL consents │
  └────────────────┘

  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
  │Keycloak (8080) │ │MinIO (9000)    │ │Ollama (11434)  │
  │- Auth/RBAC    │ │- S3 Storage    │ │- Local LLM     │
  │- Token mgmt    │ │- PDFs, Docs    │ │- Zero latency  │
  └────────────────┘ └────────────────┘ └────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose 2.0+
- Python 3.11+ (for local dev)
- Node.js 18+ (for frontend)
- Git

### Local Development (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/sacdas2110/agentic-investment-platform.git
cd agentic-investment-platform

# 2. Start all services
cd infra
docker-compose up -d

# 3. Wait for services to be healthy
sleep 30

# 4. Run database migrations
cd ..
python scripts/migrations/run_migrations.py

# 5. Access the platform
# API Gateway: http://localhost:8000
# Analyst Portal: http://localhost:3000
# Keycloak Admin: http://localhost:8080/admin (admin/admin)
# Metabase: http://localhost:3000 (credentials in docker-compose.yml)
# Ollama: http://localhost:11434
```

### Default Credentials

| Service | Username | Password |
|---------|----------|----------|
| Keycloak | admin | admin |
| Analyst Portal | analyst@investment.local | changeme |
| MinIO | minioadmin | minioadmin |
| Metabase | admin@example.com | changeme |

## 🤖 Service Overview

### 1. API Gateway (Port 8000)
**Role**: Central request router and validator
- Request/response transformation
- JWT token validation
- Rate limiting (100 req/min per user)
- CORS handling
- Health checks

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "timestamp": "2024-07-01T12:00:00Z"}
```

### 2. Ingestion Agent (Port 8001)
**Role**: Document processing and entity extraction
- OCR (Tesseract) for scanned documents
- Entity extraction (companies, sectors, geographies, KPIs)
- Embedding generation for RAG
- Metadata enrichment

```python
POST /api/v1/documents/upload
{
  "file": "<binary>",
  "document_type": "research_report"
}
```

### 3. Document Intelligence Agent (Port 8002)
**Role**: NLP analysis of investment documents
- Abstractive summarization
- Key insight extraction
- Risk flag identification
- Sentiment analysis
- Strategy signal detection

Model: `facebook/bart-large-cnn` (HuggingFace)

### 4. Research RAG Agent (Port 8003)
**Role**: Semantic search and synthesis
- Qdrant vector similarity search
- Multi-document cross-referencing
- Investment thesis generation
- GCC/Dubai market context

```python
POST /api/v1/research/synthesize
{
  "query": "Tech sector investments in Dubai",
  "top_k": 10
}
```

### 5. Investment Scorer (Port 8004)
**Role**: ML-based opportunity scoring
- XGBoost model inference
- Multi-factor scoring (0-100)
- SHAP explainability
- Risk/return assessment
- ESG scoring

```python
POST /api/v1/investments/score
{
  "investment_id": "inv-123"
}
# Response: {"score": 75.5, "recommendation": "buy", "drivers": [...]}
```

### 6. Portfolio Analytics Agent (Port 8005)
**Role**: Advanced portfolio analysis
- Prophet/ARIMA forecasting
- Scenario modeling (base/upside/downside)
- Monte Carlo stress testing
- Mean-variance optimization
- Exposure heatmaps

### 7. Risk Monitor Agent (Port 8006)
**Role**: Real-time risk detection
- Anomaly detection (Z-score, Isolation Forest)
- Drawdown alerts
- Volatility spike detection
- FX shock monitoring
- Correlation break detection

Latency: 100-200ms per alert

### 8. Briefing Generator (Port 8007)
**Role**: Executive dossier creation
- Local LLM synthesis (Ollama)
- Investment narrative generation
- Risk/return storytelling
- Market forecast integration
- PDF generation (WeasyPrint)

```python
POST /api/v1/briefs/generate
{
  "investment_id": "inv-123",
  "format": "pdf"
}
# Returns: S3 URL to PDF brief
```

### 9. Compliance & Governance (Port 8008)
**Role**: PDPL compliance enforcement
- Consent verification
- Append-only audit logging
- PII encryption/decryption
- Data minimization scheduling
- RBAC enforcement

## 📊 Data Flow

### Complete Investment Analysis Workflow

```
1. Analyst uploads PDF
   └─> API Gateway validates
       └─> Ingestion Agent (8001)
           - Extract text (OCR)
           - Parse entities
           - Generate embeddings
           ├─ Emit: investment.ingested
           
2. Kafka consumes investment.ingested
   ├─> Document Intel Agent (8002)
   │   - Summarize
   │   - Extract insights
   │   - Analyze sentiment
   │   └─ Emit: document.analyzed
   │
   └─> Research RAG Agent (8003)
       - Query Qdrant for similar docs
       - Synthesize thesis
       └─ Emit: research.generated

3. Later: Portfolio context available
   └─> Investment Scorer (8004)
       - Load analysis results
       - Run XGBoost model
       - Extract SHAP drivers
       └─ Emit: investment.scored

4. Async processing
   ├─> Portfolio Analytics (8005)
   │   - Forecast returns
   │   - Run stress tests
   │   └─ Emit: portfolio.analyzed
   │
   └─> Risk Monitor (8006)
       - Monitor market data
       - Detect anomalies
       └─ Emit: risk.detected

5. On-demand: Generate briefing
   └─> Briefing Generator (8007)
       - Collect all outputs
       - Call Ollama for narrative
       - Generate PDF
       └─ Emit: briefing.generated

6. All events logged
   └─> Compliance & Governance (8008)
       - Append to audit log
       - Verify PDPL consent
       - Encrypt PII

7. Analyst Portal displays
   └─> Real-time dashboard
       - Investment summary
       - Risk flags
       - Score + drivers
       - PDF brief download
```

## 🚀 Deployment

### Docker Compose (Development)

```bash
cd infra
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

### Kubernetes (Production)

```bash
# Create namespace and secrets
kubectl apply -f infra/kubernetes/namespace-config.yaml

# Deploy services
kubectl apply -f infra/kubernetes/

# Check rollout
kubectl rollout status deployment/api-gateway -n investment-platform

# View pods
kubectl get pods -n investment-platform

# Scale service
kubectl scale deployment/api-gateway --replicas=5 -n investment-platform
```

## 📚 API Documentation

### OpenAPI/Swagger

All services expose Swagger UI:

- **API Gateway**: http://localhost:8000/docs
- **Ingestion Agent**: http://localhost:8001/docs
- **Document Intel**: http://localhost:8002/docs
- etc.

### Authentication

All endpoints (except `/health`) require JWT token:

```bash
# 1. Get token from Keycloak
TOKEN=$(curl -X POST http://localhost:8080/realms/investment_platform/protocol/openid-connect/token \
  -d "client_id=api_gateway" \
  -d "client_secret=changeme" \
  -d "grant_type=client_credentials" \
  | jq -r '.access_token')

# 2. Use token
curl http://localhost:8000/api/v1/investments \
  -H "Authorization: Bearer $TOKEN"
```

### Core Endpoints

#### Investments
```
GET    /api/v1/investments              # List all
GET    /api/v1/investments/{id}         # Get details
POST   /api/v1/investments              # Create new
PATCH  /api/v1/investments/{id}         # Update
DELETE /api/v1/investments/{id}         # Delete
GET    /api/v1/investments/{id}/score   # Get score
```

#### Portfolios
```
GET    /api/v1/portfolios               # List user's portfolios
POST   /api/v1/portfolios               # Create portfolio
GET    /api/v1/portfolios/{id}          # Get details
GET    /api/v1/portfolios/{id}/analyze  # Get analytics
GET    /api/v1/portfolios/{id}/forecast # Get forecast
```

#### Documents
```
POST   /api/v1/documents/upload         # Upload document
GET    /api/v1/documents                # List documents
GET    /api/v1/documents/{id}           # Get details
DELETE /api/v1/documents/{id}           # Delete
```

#### Research
```
POST   /api/v1/research/synthesize      # RAG search + synthesis
GET    /api/v1/research/similar/{id}    # Find similar investments
```

#### Briefs
```
POST   /api/v1/briefs/generate          # Generate investment brief
GET    /api/v1/briefs/{id}              # Get brief
GET    /api/v1/briefs/{id}/pdf          # Download PDF
```

#### Risk
```
GET    /api/v1/risk/alerts              # Get active alerts
GET    /api/v1/risk/portfolio/{id}      # Portfolio risk metrics
```

#### Compliance
```
GET    /api/v1/compliance/consent/{user_id}   # Get user consents
POST   /api/v1/compliance/consent               # Record consent
GET    /api/v1/audit-logs                      # Audit trail (admin)
```

## ⚙️ Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://investment_user:password@localhost:5432/investment_db
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379/0

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=changeme

# Keycloak
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=investment_platform
KEYCLOAK_CLIENT_ID=api_gateway
KEYCLOAK_CLIENT_SECRET=changeme

# S3/MinIO
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=investment-briefs

# LLM
LLM_HOST=http://localhost:11434
LLM_MODEL=llama2  # or mistral, neural-chat, etc.

# Security
JWT_SECRET=your_super_secret_key_change_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Logging
LOG_LEVEL=INFO
```

### Copy Example File

```bash
cp .env.example .env
# Edit .env with your values
```

## 🔐 Compliance

### PDPL (Personal Data Protection Law)

✅ **Implemented Controls**:
- Consent verification on all endpoints
- Append-only audit logs (7-year retention)
- PII encryption at rest (pgcrypto AES-256)
- Data minimization scheduling (weekly)
- Cross-border transfer controls
- Breach notification procedures

### Audit Logs

```sql
-- View audit trail
SELECT * FROM audit.audit_logs 
WHERE resource_type = 'investment'
ORDER BY timestamp DESC
LIMIT 100;
```

### Data Access Request

```python
POST /api/v1/compliance/data-access-request
{
  "user_email": "analyst@company.com",
  "request_type": "export"  # or "delete", "rectify"
}
```

## 📦 Technologies

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **Backend** | Python 3.11 + FastAPI | Microservices |
| **Frontend** | Next.js 14 + React 18 | Analyst Portal |
| **Database** | PostgreSQL 15 | Relational data |
| **Vectors** | Qdrant | Semantic search (RAG) |
| **Cache** | Redis 7 | Session + Rate limiting |
| **Message Queue** | Apache Kafka 7.5 | Event orchestration |
| **Auth** | Keycloak 22 | OAuth2/OIDC |
| **Storage** | MinIO | S3-compatible |
| **LLM** | Ollama | Local inference |
| **ML Models** | HuggingFace, XGBoost, Prophet | Analysis + Forecasting |
| **Orchestration** | Kubernetes, Docker Compose | Deployment |
| **Monitoring** | Prometheus, ELK | Observability |
| **CI/CD** | GitHub Actions | Automation |

## 📖 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design, layers, data flow
- **[Agent Orchestration](docs/AGENT_ORCHESTRATION.md)** - Event protocols, handoff patterns
- **[Data Governance](docs/DATA_GOVERNANCE.md)** - PDPL compliance, encryption, audit logs
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Onboarding, development setup, debugging

## 🔄 CI/CD Pipeline

### Automated Workflows

**On Push to Main**:
1. Lint & test all services
2. Build Docker images
3. Push to container registry
4. Run database migrations
5. Deploy to Kubernetes
6. Notify Slack on success/failure

```bash
# View workflow runs
git log --oneline | head

# Manual trigger
gh workflow run ci-cd.yml
```

## 🤝 Contributing

### Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes and test**
   ```bash
   pytest services/api-gateway/tests/
   ```

3. **Format code**
   ```bash
   black services/ --line-length=120
   isort services/
   ```

4. **Commit and push**
   ```bash
   git commit -m "feat: add investment scoring"
   git push origin feature/my-feature
   ```

5. **Create Pull Request**
   - Fill PR template
   - Link to relevant issues
   - Wait for CI/CD to pass
   - Request review

### Code Standards

- Python: PEP 8 (enforced via black, flake8)
- TypeScript: ESLint + Prettier
- Docstrings: Google style
- Tests: Minimum 80% coverage
- Commits: Conventional Commits (feat:, fix:, docs:, etc.)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sacdas2110/agentic-investment-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sacdas2110/agentic-investment-platform/discussions)
- **Email**: dpo@investment-platform.local
- **Slack**: [Join our community](https://join.slack.com/share/...)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI models from [HuggingFace](https://huggingface.co/)
- Vector search via [Qdrant](https://qdrant.tech/)
- Event streaming via [Apache Kafka](https://kafka.apache.org/)
- Infrastructure as Code with [Docker](https://www.docker.com/) & [Kubernetes](https://kubernetes.io/)

---

**Last Updated**: July 1, 2024  
**Platform Version**: 1.0.0  
**Status**: Active Development 🚀
