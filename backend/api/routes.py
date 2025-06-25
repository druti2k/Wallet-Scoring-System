import time
from fastapi import APIRouter, HTTPException, Request, Query, Depends
from langchain_tools.assistant import handle_user_query
from blockchain.wallet_analyzer import WalletAnalyzer
from blockchain.data_fetcher import DataFetcher
from typing import Optional
from config import settings
from utils.logger import get_logger, log_wallet_analysis, log_api_call
from utils.cache import (
    cache_wallet_analysis, get_cached_wallet_analysis,
    cache_transaction_data, get_cached_transaction_data,
    cache_defi_data, get_cached_defi_data
)
from utils.monitoring import (
    WALLET_ANALYSIS_COUNT, WALLET_ANALYSIS_DURATION,
    API_CALL_COUNT, API_CALL_DURATION
)

logger = get_logger(__name__)
router = APIRouter()

@router.post("/assistant/query")
async def assistant_query(request: Request):
    """Handle natural language queries via LangChain"""
    data = await request.json()
    query = data.get("query")
    
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        logger.info("Processing assistant query", query_length=len(query))
        response = handle_user_query(query)
        
        return {
            "success": True,
            "response": response,
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    except Exception as e:
        logger.error("Assistant query failed", error=str(e), query=query)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/wallet/{address}")
async def analyze_wallet(
    address: str, 
    network: str = Query("ethereum", description="Blockchain network"),
    request: Request = None
):
    """Analyze a wallet address and return comprehensive scoring"""
    start_time = time.time()
    
    try:
        # Check cache first
        cached_result = get_cached_wallet_analysis(address, network)
        if cached_result:
            logger.info("Returning cached wallet analysis", wallet_address=address, network=network)
            WALLET_ANALYSIS_COUNT.labels(network=network, status="cached").inc()
            return {
                "success": True,
                "data": cached_result,
                "cached": True,
                "request_id": getattr(request.state, "request_id", "unknown")
            }
        
        logger.info("Starting wallet analysis", wallet_address=address, network=network)
        
        # Perform analysis
        analyzer = WalletAnalyzer()
        result = analyzer.analyze_wallet(address, network)
        
        if not result.get("success", True):
            WALLET_ANALYSIS_COUNT.labels(network=network, status="failed").inc()
            raise HTTPException(status_code=400, detail=result.get("error", "Analysis failed"))
        
        # Cache the result
        cache_wallet_analysis(address, network, result)
        
        # Record metrics
        duration = time.time() - start_time
        WALLET_ANALYSIS_COUNT.labels(network=network, status="success").inc()
        WALLET_ANALYSIS_DURATION.labels(network=network).observe(duration)
        
        # Log analysis completion
        trust_score = result.get("trust_score", 0)
        log_wallet_analysis(address, network, trust_score, duration)
        
        # Transform result to match frontend expectations
        summary = result.get("summary", {})
        etherscan = result.get("data_sources", {}).get("etherscan", {})
        transactions = etherscan.get("transactions", [])
        # Calculate total value and avg transaction value
        total_value = sum(float(tx.get("value", 0)) for tx in transactions) if transactions else 0
        avg_transaction = total_value / len(transactions) if transactions else 0
        # Prepare recent transactions (take up to 10 most recent)
        recent_transactions = []
        for tx in transactions[:10]:
            recent_transactions.append({
                "id": tx.get("hash", ""),
                "hash": tx.get("hash", ""),
                "type": "incoming" if tx.get("to", "").lower() == address.lower() else "outgoing",
                "amount": tx.get("value", "0"),
                "value": tx.get("value", "0"),
                "to": tx.get("to", ""),
                "from": tx.get("from", ""),
                "timestamp": tx.get("timeStamp", ""),
                "gas": tx.get("gas", "")
            })
        # Prepare activities (empty for now)
        activities = []
        # Prepare metrics (empty for now)
        metrics = []
        # Calculate activeSince (from oldest transaction)
        if transactions:
            oldest = min(transactions, key=lambda tx: int(tx.get("timeStamp", "0") or 0))
            from datetime import datetime
            active_since = datetime.utcfromtimestamp(int(oldest.get("timeStamp", "0"))).strftime("%Y-%m-%d")
        else:
            active_since = ""
        wallet_data = {
            "score": result.get("trust_score", 0),
            "address": result.get("wallet_address", address),
            "metrics": metrics,
            "recentTransactions": recent_transactions,
            "activities": activities,
            "totalValue": str(total_value),
            "transactionCount": summary.get("total_transactions", 0),
            "avgTransaction": str(avg_transaction),
            "activeSince": active_since,
            # Optionally include other fields as needed
        }
        return {
            "success": True,
            "data": wallet_data,
            "cached": False,
            "request_id": getattr(request.state, "request_id", "unknown")
        }
        
    except ValueError as e:
        WALLET_ANALYSIS_COUNT.labels(network=network, status="failed").inc()
        logger.error("Wallet analysis validation error", wallet_address=address, error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        WALLET_ANALYSIS_COUNT.labels(network=network, status="failed").inc()
        logger.error("Wallet analysis failed", wallet_address=address, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/wallet/{address}/transactions")
async def get_wallet_transactions(
    address: str, 
    network: str = Query("ethereum", description="Blockchain network"),
    request: Request = None
):
    """Get transaction history for a wallet"""
    start_time = time.time()
    
    try:
        # Check cache first
        cached_result = get_cached_transaction_data(address, network)
        if cached_result:
            logger.info("Returning cached transaction data", wallet_address=address, network=network)
            return {
                "success": True,
                "data": cached_result,
                "cached": True,
                "request_id": getattr(request.state, "request_id", "unknown")
            }
        
        logger.info("Fetching transaction data", wallet_address=address, network=network)
        
        # Fetch data
        fetcher = DataFetcher()
        result = fetcher.fetch_from_etherscan(address)
        
        if not result.get("success", True):
            API_CALL_COUNT.labels(api_name="etherscan", status="failed").inc()
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to fetch transactions"))
        
        # Cache the result
        cache_transaction_data(address, network, result)
        
        # Record metrics
        duration = time.time() - start_time
        API_CALL_COUNT.labels(api_name="etherscan", status="success").inc()
        API_CALL_DURATION.labels(api_name="etherscan").observe(duration)
        
        return {
            "success": True,
            "data": result,
            "cached": False,
            "request_id": getattr(request.state, "request_id", "unknown")
        }
        
    except Exception as e:
        API_CALL_COUNT.labels(api_name="etherscan", status="failed").inc()
        logger.error("Transaction fetch failed", wallet_address=address, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/wallet/{address}/balance")
async def get_wallet_balance(
    address: str, 
    network: str = Query("ethereum", description="Blockchain network"),
    request: Request = None
):
    """Get current balance for a wallet"""
    start_time = time.time()
    
    try:
        logger.info("Fetching wallet balance", wallet_address=address, network=network)
        
        fetcher = DataFetcher()
        result = fetcher.get_wallet_balance(address, network)
        
        if not result.get("success", True):
            API_CALL_COUNT.labels(api_name="rpc", status="failed").inc()
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to fetch balance"))
        
        # Record metrics
        duration = time.time() - start_time
        API_CALL_COUNT.labels(api_name="rpc", status="success").inc()
        API_CALL_DURATION.labels(api_name="rpc").observe(duration)
        
        return {
            "success": True,
            "data": result,
            "request_id": getattr(request.state, "request_id", "unknown")
        }
        
    except Exception as e:
        API_CALL_COUNT.labels(api_name="rpc", status="failed").inc()
        logger.error("Balance fetch failed", wallet_address=address, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/wallet/{address}/defi")
async def get_wallet_defi_activity(
    address: str,
    request: Request = None
):
    """Get DeFi activity for a wallet"""
    start_time = time.time()
    
    try:
        # Check cache first
        cached_result = get_cached_defi_data(address)
        if cached_result:
            logger.info("Returning cached DeFi data", wallet_address=address)
            return {
                "success": True,
                "data": cached_result,
                "cached": True,
                "request_id": getattr(request.state, "request_id", "unknown")
            }
        
        logger.info("Fetching DeFi activity", wallet_address=address)
        
        fetcher = DataFetcher()
        result = fetcher.fetch_from_the_graph(address)
        
        if not result.get("success", True):
            API_CALL_COUNT.labels(api_name="the_graph", status="failed").inc()
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to fetch DeFi data"))
        
        # Cache the result
        cache_defi_data(address, result)
        
        # Record metrics
        duration = time.time() - start_time
        API_CALL_COUNT.labels(api_name="the_graph", status="success").inc()
        API_CALL_DURATION.labels(api_name="the_graph").observe(duration)
        
        return {
            "success": True,
            "data": result,
            "cached": False,
            "request_id": getattr(request.state, "request_id", "unknown")
        }
        
    except Exception as e:
        API_CALL_COUNT.labels(api_name="the_graph", status="failed").inc()
        logger.error("DeFi data fetch failed", wallet_address=address, error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-22T12:00:00Z",
        "version": "1.0.0"
    }

@router.get("/api-keys/status")
async def check_api_keys(request: Request = None):
    """Check status of configured API keys"""
    keys_status = {
        "openai": bool(settings.openai_api_key),
        "etherscan": bool(settings.etherscan_api_key),
        "alchemy": bool(settings.alchemy_api_key),
        "the_graph": bool(settings.the_graph_api_key)
    }
    
    return {
        "success": True,
        "api_keys": keys_status,
        "configured_count": sum(keys_status.values()),
        "total_count": len(keys_status),
        "request_id": getattr(request.state, "request_id", "unknown")
    }