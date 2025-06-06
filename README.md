# Behavioral Wallet Scoring System

## Overview
The Behavioral Wallet Scoring System is an AI-powered solution designed to analyze on-chain wallet behavior for fraud detection, risk assessment, and user pattern explanation. This project leverages advanced data science techniques, machine learning models, and blockchain technology to provide insights into wallet trustworthiness and transaction anomalies.

## Technical Stack
- **Backend Framework:** FastAPI
- **Programming Language:** Python
- **Machine Learning:** scikit-learn, SHAP
- **Data Processing:** pandas, numpy
- **Blockchain Interaction:** web3.py, The Graph, Etherscan, Alchemy
- **Natural Language Processing:** LangChain, OpenAI
- **Visualization:** matplotlib
- **API Testing & Docs:** Swagger UI (FastAPI `/docs`)
- **Environment:** Jupyter Notebook (for experiments)
- **Web Server:** Uvicorn
- **Frontend Framework:** React

## Features
- **Wallet Trustworthiness Evaluation**: Assess the reliability of wallets based on their on-chain behavior.
- **Fraud Detection**: Identify suspicious activities and potential fraud in wallet transactions.
- **User Pattern Analysis**: Understand user behavior through clustering and scoring mechanisms.
- **Natural Language Interface**: Interact with the system using natural language queries via LangChain.

## Architecture
The system is structured into several components:
- **API**: Handles incoming requests and serves endpoints for wallet scoring and analysis.
- **Machine Learning**: Implements models for clustering, fraud detection, and SHAP for interpretability.
- **Blockchain Interaction**: Fetches on-chain data from various sources and analyzes wallet behavior.
- **LangChain Integration**: Provides a conversational interface for users to interact with the scoring system.
- **Frontend**: A React application that communicates with the FastAPI backend to provide a user-friendly interface.

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd behavioral-wallet-scoring
pip install -r requirements.txt
```

### Frontend (React)

To set up the React frontend:

```bash
cd frontend
npm install
npm start
```

The frontend will run at [http://localhost:3000](http://localhost:3000) and can communicate with the FastAPI backend.

## Usage
Run the application using the following command:

```bash
python src/main.py
```

Once the server is running, you can access the API endpoints to evaluate wallet scores, detect fraud, and analyze user patterns. The frontend can be accessed in a web browser at [http://localhost:3000](http://localhost:3000).

## Contributing
Contributions