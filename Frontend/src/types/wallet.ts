export type NetworkType = 'ethereum' | 'bitcoin' | 'solana' | 'polygon' | 'binance';

export interface Transaction {
  id: string;
  hash: string;
  type: 'incoming' | 'outgoing';
  amount: string;
  value: string;
  to: string;
  from: string;
  timestamp: string;
  gas: string;
}

export interface WalletMetric {
  id: string;
  name: string;
  score: number;
  description: string;
}

export interface Activity {
  id: string;
  type: 'transaction' | 'contract';
  description: string;
  timestamp: string;
  highlight: boolean;
}

export interface WalletData {
  address: string;
  network: NetworkType;
  score: number;
  riskLevel: 'low' | 'medium' | 'high';
  totalValue: string;
  transactionCount: number;
  avgTransaction: string;
  activeSince: string;
  metrics: WalletMetric[];
  recentTransactions: Transaction[];
  activities: Activity[];
  lastUpdated: string;
}