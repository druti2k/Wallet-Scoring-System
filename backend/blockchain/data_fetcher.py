import requests
import asyncio
import aiohttp
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from web3 import Web3
from dotenv import load_dotenv
import time
import json

load_dotenv()

class DataFetcher:
    def __init__(self):
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
        self.alchemy_api_key = os.getenv("ALCHEMY_API_KEY")
        self.the_graph_api_key = os.getenv("THE_GRAPH_API_KEY")
        
        # Initialize Web3 connections
        self.ethereum_w3 = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC_URL")))
        self.polygon_w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC_URL")))
        self.bsc_w3 = Web3(Web3.HTTPProvider(os.getenv("BSC_RPC_URL")))
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
    def _rate_limit(self):
        """Implement rate limiting to avoid API limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def fetch_from_etherscan(self, address: str, start_block: int = 0, end_block: int = 99999999) -> Dict[str, Any]:
        """Fetch transaction data from Etherscan API"""
        if not self.etherscan_api_key:
            return {"error": "Etherscan API key not configured"}
        
        self._rate_limit()
        
        try:
            # Get normal transactions
            url = f"https://api.etherscan.io/api"
            params = {
                "module": "account",
                "action": "txlist",
                "address": address,
                "startblock": start_block,
                "endblock": end_block,
                "sort": "desc",
                "apikey": self.etherscan_api_key
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "1":
                return {
                    "success": True,
                    "transactions": data["result"],
                    "count": len(data["result"])
                }
            else:
                return {
                    "success": False,
                    "error": data.get("message", "Unknown error"),
                    "transactions": []
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "transactions": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "transactions": []
            }

    def fetch_from_alchemy(self, address: str) -> Dict[str, Any]:
        """Fetch comprehensive data from Alchemy API"""
        if not self.alchemy_api_key:
            return {"error": "Alchemy API key not configured"}
        
        self._rate_limit()
        
        try:
            url = f"https://eth-mainnet.alchemyapi.io/v2/{self.alchemy_api_key}/getAssetTransfers"
            params = {
                "fromBlock": "0x0",
                "toBlock": "latest",
                "fromAddress": address,
                "category": ["external", "internal", "erc20", "erc721", "erc1155"],
                "maxCount": "100"
            }
            
            response = requests.post(url, json=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "transfers": data.get("result", {}).get("transfers", []),
                "count": len(data.get("result", {}).get("transfers", []))
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "transfers": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "transfers": []
            }

    def fetch_from_the_graph(self, address: str) -> Dict[str, Any]:
        """Fetch DeFi protocol data from The Graph"""
        if not self.the_graph_api_key:
            return {"error": "The Graph API key not configured"}
        
        self._rate_limit()
        
        try:
            # Example query for Uniswap V2 transactions
            query = """
            {
              swaps(where: {to: "%s"}, orderBy: timestamp, orderDirection: desc, first: 100) {
                id
                timestamp
                pair {
                  token0 {
                    symbol
                  }
                  token1 {
                    symbol
                  }
                }
                amount0In
                amount1In
                amount0Out
                amount1Out
              }
            }
            """ % address
            
            url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
            response = requests.post(url, json={"query": query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "defi_transactions": data.get("data", {}).get("swaps", []),
                "count": len(data.get("data", {}).get("swaps", []))
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "defi_transactions": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "defi_transactions": []
            }

    def get_wallet_balance(self, address: str, network: str = "ethereum") -> Dict[str, Any]:
        """Get wallet balance and token holdings"""
        try:
            if network == "ethereum":
                w3 = self.ethereum_w3
            elif network == "polygon":
                w3 = self.polygon_w3
            elif network == "bsc":
                w3 = self.bsc_w3
            else:
                return {"error": f"Unsupported network: {network}"}
            
            if not w3.is_connected():
                return {"error": f"Failed to connect to {network} network"}
            
            # Get native token balance
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            
            return {
                "success": True,
                "network": network,
                "address": address,
                "native_balance": str(balance_eth),
                "native_balance_wei": str(balance_wei),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get balance: {str(e)}"
            }

    def get_wallet_data(self, address: str, network: str = "ethereum") -> Dict[str, Any]:
        """Get comprehensive wallet data from all sources"""
        print(f"Fetching data for wallet: {address} on {network}")
        
        # Validate address
        if not Web3.is_address(address):
            return {
                "success": False,
                "error": "Invalid wallet address"
            }
        
        # Fetch data from all sources
        etherscan_data = self.fetch_from_etherscan(address)
        alchemy_data = self.fetch_from_alchemy(address)
        the_graph_data = self.fetch_from_the_graph(address)
        balance_data = self.get_wallet_balance(address, network)
        
        # Compile results
        result = {
            "wallet_address": address,
            "network": network,
            "timestamp": datetime.now().isoformat(),
            "data_sources": {
            "etherscan": etherscan_data,
                "alchemy": alchemy_data,
                "the_graph": the_graph_data,
                "balance": balance_data
            },
            "summary": {
                "total_transactions": len(etherscan_data.get("transactions", [])),
                "total_transfers": len(alchemy_data.get("transfers", [])),
                "defi_transactions": len(the_graph_data.get("defi_transactions", [])),
                "has_balance": balance_data.get("success", False)
            }
        }
        
        return result

    def analyze_transaction_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze transaction patterns for risk assessment"""
        if not transactions:
            return {"error": "No transactions to analyze"}
        
        try:
            # Calculate basic statistics
            total_transactions = len(transactions)
            total_value = sum(float(tx.get("value", 0)) for tx in transactions)
            avg_value = total_value / total_transactions if total_transactions > 0 else 0
            
            # Analyze transaction frequency
            timestamps = [int(tx.get("timeStamp", 0)) for tx in transactions]
            if timestamps:
                timestamps.sort()
                time_span = timestamps[-1] - timestamps[0] if len(timestamps) > 1 else 0
                avg_daily_transactions = total_transactions / (time_span / 86400 + 1)  # 86400 seconds in a day
            else:
                avg_daily_transactions = 0
            
            # Analyze unique addresses
            unique_to_addresses = len(set(tx.get("to", "") for tx in transactions))
            unique_from_addresses = len(set(tx.get("from", "") for tx in transactions))
            
            return {
                "success": True,
                "total_transactions": total_transactions,
                "total_value_eth": total_value,
                "average_value_eth": avg_value,
                "average_daily_transactions": avg_daily_transactions,
                "unique_to_addresses": unique_to_addresses,
                "unique_from_addresses": unique_from_addresses,
                "transaction_span_days": time_span / 86400 if time_span > 0 else 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to analyze patterns: {str(e)}"
            }

# Example usage and testing
if __name__ == "__main__":
    fetcher = DataFetcher()
    
    # Test with a known wallet address (Vitalik's wallet)
    test_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    print("Testing data fetcher...")
    result = fetcher.get_wallet_data(test_address)
    print(json.dumps(result, indent=2))