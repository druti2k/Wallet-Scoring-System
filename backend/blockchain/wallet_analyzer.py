from web3 import Web3
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .data_fetcher import DataFetcher
import json

class WalletAnalyzer:
    def __init__(self, web3_provider: str = None):
        self.data_fetcher = DataFetcher()
        self.web3 = Web3(Web3.HTTPProvider(web3_provider)) if web3_provider else None

    def analyze_wallet(self, wallet_address: str, network: str = "ethereum") -> Dict[str, Any]:
        """Comprehensive wallet analysis with real data"""
        if not Web3.is_address(wallet_address):
            raise ValueError("Invalid wallet address")

        print(f"Starting analysis for wallet: {wallet_address}")
        
        # Fetch comprehensive data
        wallet_data = self.data_fetcher.get_wallet_data(wallet_address, network)
        
        if not wallet_data.get("success", True):
            return {
                "wallet_address": wallet_address,
                "success": False,
                "error": wallet_data.get("error", "Failed to fetch wallet data")
            }

        # Extract transactions for analysis
        transactions = wallet_data["data_sources"]["etherscan"].get("transactions", [])
        
        # Perform risk assessment
        risk_score = self.assess_risk(transactions, wallet_data)
        anomalies = self.detect_anomalies(transactions, wallet_data)
        patterns = self.analyze_patterns(transactions, wallet_data)
        
        # Calculate trust score
        trust_score = self.calculate_trust_score(risk_score, patterns, wallet_data)

        return {
            "wallet_address": wallet_address,
            "network": network,
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "trust_score": trust_score,
            "risk_score": risk_score,
            "anomalies": anomalies,
            "patterns": patterns,
            "summary": wallet_data["summary"],
            "data_sources": wallet_data["data_sources"]
        }

    def assess_risk(self, transactions: List[Dict], wallet_data: Dict) -> Dict[str, Any]:
        """Assess risk based on transaction patterns and wallet behavior"""
        if not transactions:
            return {"risk_level": "unknown", "risk_score": 0, "factors": []}
        
        risk_factors = []
        risk_score = 0
        
        # Analyze transaction patterns
        pattern_analysis = self.data_fetcher.analyze_transaction_patterns(transactions)
        
        if pattern_analysis.get("success"):
            # Factor 1: Transaction frequency (high frequency = higher risk)
            avg_daily_tx = pattern_analysis["average_daily_transactions"]
            if avg_daily_tx > 10:
                risk_factors.append("High transaction frequency")
                risk_score += 20
            elif avg_daily_tx > 5:
                risk_factors.append("Moderate transaction frequency")
                risk_score += 10
            
            # Factor 2: Transaction value patterns
            avg_value = pattern_analysis["average_value_eth"]
            if avg_value > 10:  # High value transactions
                risk_factors.append("High value transactions")
                risk_score += 15
            elif avg_value < 0.001:  # Very small transactions
                risk_factors.append("Micro-transactions")
                risk_score += 5
            
            # Factor 3: Address diversity
            unique_addresses = pattern_analysis["unique_to_addresses"]
            if unique_addresses > 100:
                risk_factors.append("High address diversity")
                risk_score += 15
            elif unique_addresses < 5:
                risk_factors.append("Low address diversity")
                risk_score += 5
        
        # Factor 4: DeFi interactions
        defi_tx_count = wallet_data["summary"]["defi_transactions"]
        if defi_tx_count > 50:
            risk_factors.append("Heavy DeFi usage")
            risk_score += 10
        elif defi_tx_count > 10:
            risk_factors.append("Moderate DeFi usage")
            risk_score += 5
        
        # Factor 5: Wallet age
        if pattern_analysis.get("success"):
            wallet_age_days = pattern_analysis["transaction_span_days"]
            if wallet_age_days < 30:
                risk_factors.append("New wallet")
                risk_score += 20
            elif wallet_age_days < 90:
                risk_factors.append("Relatively new wallet")
                risk_score += 10
            elif wallet_age_days > 365:
                risk_factors.append("Established wallet")
                risk_score -= 10  # Reduce risk for old wallets
        
        # Factor 6: Balance analysis
        balance_data = wallet_data["data_sources"]["balance"]
        if balance_data.get("success"):
            balance_eth = float(balance_data["native_balance"])
            if balance_eth > 100:
                risk_factors.append("High balance")
                risk_score += 5
            elif balance_eth < 0.01:
                risk_factors.append("Very low balance")
                risk_score += 10
        
        # Normalize risk score to 0-100
        risk_score = max(0, min(100, risk_score))
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "factors": risk_factors,
            "pattern_analysis": pattern_analysis
        }

    def detect_anomalies(self, transactions: List[Dict], wallet_data: Dict) -> List[Dict]:
        """Detect anomalous patterns in transactions"""
        anomalies = []
        
        if not transactions:
            return anomalies
        
        # Convert to pandas for easier analysis
        df = pd.DataFrame(transactions)
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
        
        # Anomaly 1: Unusual transaction values
        if len(df) > 0:
            value_mean = df['value'].mean()
            value_std = df['value'].std()
            
            # Find transactions with values > 2 standard deviations from mean
            unusual_values = df[df['value'] > (value_mean + 2 * value_std)]
            for _, tx in unusual_values.iterrows():
                anomalies.append({
                    "type": "unusual_value",
                    "description": f"Transaction value {tx['value']:.4f} ETH is unusually high",
                    "transaction_hash": tx.get('hash', ''),
                    "severity": "medium"
                })
        
        # Anomaly 2: Rapid successive transactions
        if len(df) > 1:
            df_sorted = df.sort_values('timeStamp')
            time_diffs = df_sorted['timeStamp'].diff()
            rapid_txs = time_diffs[time_diffs < timedelta(minutes=1)]
            
            if len(rapid_txs) > 0:
                anomalies.append({
                    "type": "rapid_transactions",
                    "description": f"Found {len(rapid_txs)} transactions within 1 minute of each other",
                    "severity": "low"
                })
        
        # Anomaly 3: High DeFi activity
        defi_count = wallet_data["summary"]["defi_transactions"]
        if defi_count > 100:
            anomalies.append({
                "type": "high_defi_activity",
                "description": f"Wallet has {defi_count} DeFi transactions",
                "severity": "medium"
            })
        
        return anomalies

    def analyze_patterns(self, transactions: List[Dict], wallet_data: Dict) -> Dict[str, Any]:
        """Analyze behavioral patterns"""
        patterns = {
            "transaction_patterns": {},
            "defi_usage": {},
            "balance_patterns": {},
            "activity_timeline": {}
        }
        
        if transactions:
            # Transaction pattern analysis
            pattern_analysis = self.data_fetcher.analyze_transaction_patterns(transactions)
            if pattern_analysis.get("success"):
                patterns["transaction_patterns"] = pattern_analysis
            
            # Activity timeline
            df = pd.DataFrame(transactions)
            if len(df) > 0:
                df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
                df['hour'] = df['timeStamp'].dt.hour
                
                # Most active hours
                active_hours = df['hour'].value_counts().head(3).to_dict()
                patterns["activity_timeline"]["most_active_hours"] = active_hours
        
        # DeFi usage patterns
        defi_data = wallet_data["data_sources"]["the_graph"]
        if defi_data.get("success") and defi_data.get("defi_transactions"):
            patterns["defi_usage"] = {
                "total_defi_transactions": len(defi_data["defi_transactions"]),
                "protocols_used": "Uniswap V2"  # Simplified for now
            }
        
        # Balance patterns
        balance_data = wallet_data["data_sources"]["balance"]
        if balance_data.get("success"):
            patterns["balance_patterns"] = {
                "current_balance": balance_data["native_balance"],
                "balance_currency": "ETH"
            }
        
        return patterns

    def calculate_trust_score(self, risk_assessment: Dict, patterns: Dict, wallet_data: Dict) -> int:
        """Calculate overall trust score (0-100)"""
        base_score = 50  # Start with neutral score
        
        # Adjust based on risk level
        risk_score = risk_assessment.get("risk_score", 50)
        if risk_score < 30:
            base_score += 30  # Low risk = high trust
        elif risk_score > 70:
            base_score -= 30  # High risk = low trust
        else:
            base_score -= (risk_score - 50) * 0.6  # Proportional adjustment
        
        # Adjust based on wallet age
        if patterns.get("transaction_patterns", {}).get("transaction_span_days", 0) > 365:
            base_score += 10  # Bonus for old wallets
        elif patterns.get("transaction_patterns", {}).get("transaction_span_days", 0) < 30:
            base_score -= 15  # Penalty for new wallets
        
        # Adjust based on transaction count
        total_tx = wallet_data["summary"]["total_transactions"]
        if total_tx > 100:
            base_score += 5  # Bonus for active wallets
        elif total_tx < 5:
            base_score -= 10  # Penalty for inactive wallets
        
        # Adjust based on balance
        balance_data = wallet_data["data_sources"]["balance"]
        if balance_data.get("success"):
            balance_eth = float(balance_data["native_balance"])
            if 0.1 <= balance_eth <= 100:
                base_score += 5  # Reasonable balance
            elif balance_eth < 0.001:
                base_score -= 5  # Very low balance
        
        # Normalize to 0-100 range
        trust_score = max(0, min(100, int(base_score)))
        
        return trust_score

# Example usage
if __name__ == "__main__":
    analyzer = WalletAnalyzer()
    
    # Test with a known wallet address
    test_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    print("Testing wallet analyzer...")
    result = analyzer.analyze_wallet(test_address)
    print(json.dumps(result, indent=2))