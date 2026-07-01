# Agentic AI Investment Intelligence Platform

**An open-source, sovereign investment intelligence system for sovereign wealth funds and institutional investors.**

## Core Principle

> *Every inbound investment query, document, dataset, or research request should be processed, analysed, summarised, and routed by specialised AI agents within seconds — producing actionable intelligence, risk insights, and investment briefs with zero analyst intervention.*

## 🏗️ System Architecture

This platform is built on an **agentic AI architecture** with:
- **Multiple specialised agents** for ingestion, analysis, scoring, risk monitoring, and briefing generation
- **Event-driven orchestration** via Kafka for asynchronous communication
- **RAG (Retrieval-Augmented Generation)** over internal investment datasets (Qdrant)
- **PDPL-compliant data governance** with full auditability
- **Role-based access control (RBAC)** via Keycloak
- **Local LLM execution** (vLLM or Ollama) for privacy and sovereignty

## 🛠️ Tech Stack

### Backend Services
- **FastAPI** – High-performance async Python framework
- **PostgreSQL** – Relational data store with pgcrypto encryption
- **Qdrant** – Vector database for document embeddings and RAG
- **Kafka** – Event streaming and agent orchestration
- **Redis** – Caching, rate limiting, session management
- **Keycloak** – Open-source identity and access management

### Frontend
- **Next.js** – React framework for analyst portal
- **Tailwind CSS** – Utility-first styling
- **Metabase** – Embedded analytics and dashboards

### ML & Data Processing
- **vLLM / Ollama** – Local LLM inference (Llama 3 / Mistral)
- **HuggingFace Transformers** – NLP models (summarization, entity extraction, sentiment)
- **XGBoost / LightGBM** – Investment scoring engine
- **Prophet / ARIMA** – Time-series forecasting
- **Tesseract OCR** – Document text extraction

### Infrastructure
- **Docker & Docker Compose** – Local development
- **Kubernetes** – Production deployment
- **GitHub Actions** – CI/CD pipelines

## 📁 Repository Structure

```
agentic-investment-platform/
├── services/
│   ├── api-gateway/                 # API orchestration, rate limiting, auth
│   ├── ingestion-agent/             # Document/dataset ingestion, OCR, entity extraction
│   ├── document-intel-agent/        # Summarization, insights, sentiment, signals
│   ├── research-rag-agent/          # RAG queries, multi-doc synthesis, thesis generation
│   ├── investment-scorer/           # ML scoring engine (XGBoost/LightGBM)
│   ├── portfolio-analytics-agent/   # Time-series forecasting, stress tests, allocation
│   ├── risk-monitor-agent/          # Real-time risk detection, anomaly detection
│   ├── briefing-generator/          # AI-generated investment dossiers (JSON + PDF)
│   └── compliance-governance/       # PDPL compliance, audit logs, consent verification
├── web/
│   └── analyst-portal/              # Next.js frontend for analysts and investors
├── infra/
│   ├── docker-compose.yml           # Local dev stack
│   ├── kubernetes/                  # K8s manifests for production
│   ├── keycloak/                    # Keycloak realm configs
│   ├── postgres/                    # DB init scripts
│   ├── redis/                       # Redis configs
│   ├── kafka/                       # Kafka broker configs
│   └── qdrant/                      # Qdrant vector DB configs
├── scripts/
│   ├── migrations/                  # Database migrations
│   └── utilities/                   # Helper scripts
├── .github/
│   └── workflows/                   # GitHub Actions CI/CD
├── docs/
│   ├── ARCHITECTURE.md              # System design overview
│   ├── AGENT_ORCHESTRATION.md       # Agent handoff protocols
│   ├── DATA_GOVERNANCE.md           # PDPL compliance details
│   └── DEVELOPER_GUIDE.md           # Onboarding guide
└── .env.example                     # Environment template
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Ollama or vLLM

### Local Development

```bash
# Clone repository
git clone https://github.com/sacdas2110/agentic-investment-platform.git
cd agentic-investment-platform

# Copy environment template
cp .env.example .env

# Start infrastructure stack
docker-compose -f infra/docker-compose.yml up -d

# Run database migrations
python scripts/migrations/run_migrations.py

# Start backend services (in separate terminals)
cd services/api-gateway && pip install -r requirements.txt && uvicorn main:app --reload

# Start frontend
cd web/analyst-portal && npm install && npm run dev

# Access at:
# - API: http://localhost:8000
# - Portal: http://localhost:3000
# - Keycloak: http://localhost:8080
```

## 📊 Agent Workflow

1. **Ingestion Agent** → Receives document/dataset → Extracts text & entities → Publishes `investment.ingested`
2. **Document Intel Agent** → Consumes event → Summarizes, flags risks, extracts signals → Publishes `document.analyzed`
3. **Research RAG Agent** → Queries Qdrant → Synthesizes multi-doc insights → Publishes `research.generated`
4. **Investment Scorer** → Scores opportunity (0–100) → Returns drivers & actions → Publishes `investment.scored`
5. **Portfolio Analytics Agent** → Forecasts, stress-tests, optimizes → Publishes `portfolio.analyzed`
6. **Risk Monitor Agent** → Detects anomalies, triggers alerts → Publishes `risk.detected`
7. **Briefing Generator** → Compiles all insights → Produces JSON + PDF dossier → Publishes `briefing.generated`
8. **Analyst Portal** → Displays all insights, enables manual refinement

## 🔐 Security & Compliance

- ✅ **PDPL Compliance**: Consent verification, data minimization, encryption (pgcrypto), audit logs
- ✅ **RBAC**: Role-based access control via Keycloak
- ✅ **Audit Trail**: Append-only logs for all data access and modifications
- ✅ **Data Sovereignty**: Local LLM inference, no external API calls
- ✅ **Encryption**: PII encrypted at rest and in transit

## 📖 Documentation

See `/docs` directory for:
- **ARCHITECTURE.md** – System design, data flow, API contracts
- **AGENT_ORCHESTRATION.md** – Event-driven protocols, handoff logic
- **DATA_GOVERNANCE.md** – PDPL compliance framework
- **DEVELOPER_GUIDE.md** – Setup, testing, deployment

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific service tests
cd services/investment-scorer && pytest

# Run integration tests
make test-integration
```

## 🐳 Docker & Kubernetes

### Local Development
```bash
docker-compose -f infra/docker-compose.yml up -d
```

### Production Deployment
```bash
# Build and push images
make build-images
make push-images

# Deploy to Kubernetes
kubectl apply -f infra/kubernetes/
```

## 📋 API Endpoints

| Service | Endpoint | Method | Purpose |
|---------|----------|--------|----------|
| Ingestion | `POST /ingest` | POST | Upload document/dataset |
| Document Intel | `POST /document-intel` | POST | Analyze document |
| Research RAG | `POST /research-query` | POST | Query research insights |
| Investment Scorer | `POST /score-investment` | POST | Score opportunity |
| Portfolio Analytics | `POST /portfolio-analytics` | POST | Run portfolio analysis |
| Risk Monitor | `GET /risk-events` | GET | Fetch risk alerts |
| Briefing Generator | `GET /briefing/{investment_id}` | GET | Generate investment brief |

## 🤝 Contributing

1. Create a feature branch
2. Make changes and test locally
3. Submit a pull request
4. Ensure CI/CD passes

## 📄 License

MIT License – See LICENSE file for details.

## 🗺️ Roadmap

- [ ] v1.0: Core agents + RAG + scoring
- [ ] v1.1: Advanced portfolio optimization
- [ ] v1.2: Real-time market data integration
- [ ] v2.0: Multi-agent consensus & debate
- [ ] v2.1: Custom LLM fine-tuning

---

**Built for sovereign investment intelligence. Open source. Zero analyst overhead.**
