import { WalletData, NetworkType } from '../types/wallet';

// This is a mock service that would typically connect to a real API
// In a production app, this would be replaced with actual API calls

export const analyzeWallet = async (address: string, network: NetworkType): Promise<WalletData> => {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  // Generate random score between 50-95
  const score = Math.floor(Math.random() * 45) + 50;
  
  // Determine risk level based on score
  let riskLevel: 'low' | 'medium' | 'high';
  if (score >= 80) {
    riskLevel = 'low';
  } else if (score >= 50) {
    riskLevel = 'medium';
  } else {
    riskLevel = 'high';
  }
  
  // Generate mock wallet data
  return {
    address,
    network,
    score,
    riskLevel,
    totalValue: '$42,839.25',
    transactionCount: 246,
    avgTransaction: '$852.14',
    activeSince: '381 days',
    metrics: [
      { id: 'tx-pattern', name: 'Transaction Patterns', score: 85, description: 'Regular, consistent transaction behavior' },
      { id: 'activity', name: 'Activity Consistency', score: 72, description: 'Some irregular patterns detected' },
      { id: 'age', name: 'Wallet Age & History', score: 93, description: 'Well-established wallet with consistent history' },
      { id: 'network', name: 'Network Interactions', score: 67, description: 'Some interactions with medium-risk addresses' },
      { id: 'volume', name: 'Transaction Volumes', score: 78, description: 'Typical transaction volumes for this wallet profile' },
      { id: 'mixing', name: 'Mixing Services Usage', score: 96, description: 'No evidence of using mixing services' },
    ],
    recentTransactions: [
      {
        id: 'tx1',
        hash: '0x8a3c5b925dfb51059b3fabf75a1f3373c2af8d4c2ab5a7370f14bdb92d5f96c6',
        type: 'outgoing',
        amount: '0.5 ETH',
        value: '$1,235.42',
        to: '0x742f...F3B2',
        from: '0x3a1b...C5D2',
        timestamp: '2025-05-14T10:24:00Z',
        gas: '0.0021 ETH'
      },
      {
        id: 'tx2',
        hash: '0x6b2d4a77e3f4b862c461e7bc2cdfc9389aa8822fe8c181f28c7d3f943ea142a7',
        type: 'incoming',
        amount: '1,250 USDT',
        value: '$1,250.00',
        to: '0x3a1b...C5D2',
        from: '0x381d...A2E1',
        timestamp: '2025-05-13T15:45:00Z',
        gas: '0.0018 ETH'
      },
    ],
    activities: [
      {
        id: 'act1',
        type: 'transaction',
        description: 'Sent 0.5 ETH to 0x742...F3B2',
        timestamp: '2025-05-14T10:24:00Z',
        highlight: false
      },
      {
        id: 'act2',
        type: 'contract',
        description: 'Interacted with Uniswap V3 contract',
        timestamp: '2025-05-13T15:45:00Z',
        highlight: false
      },
      {
        id: 'act3',
        type: 'transaction',
        description: 'Received 1,250 USDT from 0x381...A2E1',
        timestamp: '2025-05-13T12:32:00Z',
        highlight: true
      },
    ],
    lastUpdated: new Date().toISOString()
  };
};