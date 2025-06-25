# Behavioral Wallet Scoring System

## Overview
The Behavioral Wallet Scoring System is an AI-powered solution designed to analyze on-chain wallet behavior for fraud detection, risk assessment, and user pattern explanation. This project leverages advanced data science techniques, machine learning models, and blockchain technology to provide insights into wallet trustworthiness and transaction anomalies.

## 🚀 Production Ready

This system is now **production-ready** with the following enterprise-grade features:

### ✅ Production Features
- **🔒 Security**: Rate limiting, CORS, input validation, secure headers
- **📊 Monitoring**: Prometheus metrics, structured logging, health checks
- **⚡ Performance**: Redis caching, connection pooling, async processing
- **🔄 Scalability**: Docker containers, load balancing ready, horizontal scaling
- **🛡️ Reliability**: Health checks, error handling, graceful degradation
- **📈 Observability**: Request tracking, performance metrics, audit logs

### 🏗️ Architecture
- **Backend**: FastAPI with Python 3.11
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Prometheus metrics, structured logging

## Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- API Keys (OpenAI, Etherscan, Alchemy)

### 1. Clone Repository
```bash
git clone <repository-url>
cd wallet-scoring-system
```

### 2. Configure Environment
```bash
# Copy environment template
cp backend/env.example backend/.env

# Edit with your API keys and settings
nano backend/.env
```

### 3. Deploy to Production
```bash
# Run automated deployment script
./deploy.sh
```

### 4. Verify Deployment
```bash
# Run production tests
python test_production.py
```

## 📚 Documentation

- **[Production Deployment Guide](PRODUCTION.md)** - Comprehensive production setup
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs
- **[Health Check](http://localhost:8000/health)** - System health status
- **[Metrics](http://localhost:8000/metrics)** - Prometheus metrics

## Technical Stack
- **Backend Framework:** FastAPI
- **Programming Language:** Python 3.11
- **Machine Learning:** scikit-learn, SHAP
- **Data Processing:** pandas, numpy
- **Blockchain Interaction:** web3.py, The Graph, Etherscan, Alchemy
- **Natural Language Processing:** LangChain, OpenAI
- **Database:** PostgreSQL with SQLAlchemy
- **Caching:** Redis
- **Monitoring:** Prometheus, structured logging
- **Frontend:** React with TypeScript, Tailwind CSS

## Features

### 🔍 Wallet Analysis
- **Trust Score Calculation**: Multi-factor risk assessment
- **Transaction Pattern Analysis**: Behavioral clustering and anomaly detection
- **DeFi Activity Tracking**: Protocol interaction analysis
- **Risk Level Classification**: Low/Medium/High risk categorization

### 🤖 AI-Powered Insights
- **Natural Language Interface**: Chat with your wallet data
- **Pattern Recognition**: ML-powered transaction analysis
- **Fraud Detection**: Anomaly detection algorithms
- **Explainable AI**: SHAP-based model interpretability

### 📊 Real-time Data
- **Multi-chain Support**: Ethereum, Polygon, BSC
- **Live Transaction Monitoring**: Real-time blockchain data
- **Historical Analysis**: Comprehensive transaction history
- **DeFi Protocol Integration**: Uniswap, Aave, Compound, etc.

## Wallet Scoring Methodology

### Scoring Criteria
The system rates wallets based on **multiple behavioral and transactional factors**:

#### 1. **Transaction Patterns** (Weight: High)
- Regularity and consistency of transaction behavior
- Frequency of transactions over time
- Predictable patterns vs. erratic behavior
- Time-based analysis of when transactions occur

#### 2. **Activity Consistency** (Weight: Medium)
- Consistency in transaction amounts and frequency
- Regular intervals between transactions
- Stable behavior patterns over time
- Detection of unusual activity spikes

#### 3. **Wallet Age & History** (Weight: High)
- How long the wallet has been active
- Historical transaction data and patterns
- Established reputation over time
- Consistency of behavior throughout wallet's lifetime

#### 4. **Network Interactions** (Weight: Medium)
- Connections with other wallets and addresses
- Interaction with known high-risk addresses
- DeFi protocol usage and patterns
- Smart contract interactions

#### 5. **Transaction Volumes** (Weight: Medium)
- Typical transaction sizes for this wallet profile
- Volume consistency over time
- Unusual large or small transactions
- Average transaction value patterns

#### 6. **Mixing Services Usage** (Weight: High)
- Detection of mixing service interactions
- Privacy tool usage (Tornado Cash, etc.)
- Anonymization attempts
- Suspicious privacy-enhancing transactions

### Risk Level Classification
- **Low Risk (80-100)**: Normal behavior patterns, legitimate usage
- **Medium Risk (50-79)**: Some suspicious patterns, additional verification recommended  
- **High Risk (0-49)**: Multiple red flags, extreme caution required

## API Endpoints

### Core Endpoints
- `GET /api/wallet/{address}` - Analyze wallet and get trust score
- `GET /api/wallet/{address}/transactions` - Get transaction history
- `GET /api/wallet/{address}/balance` - Get current balance
- `GET /api/wallet/{address}/defi` - Get DeFi activity

### AI Assistant
- `POST /api/assistant/query` - Natural language wallet analysis

### System Endpoints
- `GET /health` - System health check
- `GET /metrics` - Prometheus metrics
- `GET /api/api-keys/status` - API key configuration status

## Development

### Local Development Setup
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

### Testing
```bash
# Run production tests
python test_production.py

# Run unit tests
pytest backend/tests/

# Run frontend tests
cd frontend && npm test
```

### Code Quality
```bash
# Backend linting
black backend/
isort backend/
flake8 backend/

# Frontend linting
cd frontend && npm run lint
```

## Deployment Options

### 1. Docker Compose (Recommended)
```bash
docker-compose up -d
```

### 2. Kubernetes
```bash
kubectl apply -f k8s/
```

### 3. Cloud Platforms
- **AWS ECS**: Container orchestration
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Managed containers

## Monitoring & Observability

### Health Checks
- Backend: `GET /health`
- Database: PostgreSQL connection check
- Cache: Redis ping
- Frontend: HTTP 200 response

### Metrics
- Request rates and latencies
- Wallet analysis performance
- Cache hit ratios
- System resource usage

### Logging
- Structured JSON logging
- Request/response tracking
- Error correlation
- Performance monitoring

## Security Features

### API Security
- Rate limiting (60 req/min, 1000 req/hour)
- Input validation and sanitization
- CORS protection
- Request ID tracking

### Data Security
- Encrypted API communications
- Secure secret management
- Database connection encryption
- Audit logging

### Infrastructure Security
- Non-root container execution
- Minimal attack surface
- Regular security updates
- Vulnerability scanning

## Performance Optimization

### Caching Strategy
- Wallet analysis: 1 hour TTL
- Transaction data: 30 minutes TTL
- DeFi activity: 30 minutes TTL
- Rate limiting: Sliding windows

### Database Optimization
- Connection pooling
- Query optimization
- Indexed queries
- Partitioned tables

### API Optimization
- Async processing
- Response compression
- Pagination
- Background tasks

## Contributing

### Development Guidelines
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with tests
4. Run the test suite: `python test_production.py`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write comprehensive tests
- Document all public APIs
- Use conventional commit messages

## Support

### Documentation
- [Production Guide](PRODUCTION.md)
- [API Documentation](http://localhost:8000/docs)
- [Troubleshooting Guide](PRODUCTION.md#troubleshooting)

### Community
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Security**: security@yourdomain.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **FastAPI** for the excellent web framework
- **OpenAI** for AI capabilities
- **Etherscan** for blockchain data
- **The Graph** for DeFi protocol data
- **React** for the frontend framework

---

**🚀 Ready for Production**: This system is designed and tested for production deployment with enterprise-grade features, security, and scalability.