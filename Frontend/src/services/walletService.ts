import { WalletData, NetworkType } from '../types/wallet';

// Service to connect to the real backend API for wallet analysis

export const analyzeWallet = async (address: string, network: NetworkType): Promise<WalletData> => {
  const response = await fetch(`/api/wallet/${address}?network=${network}`);
  if (!response.ok) {
    throw new Error('Failed to fetch wallet analysis');
  }
  const data = await response.json();
  console.log('API response:', data); // Debugging line
  if (!data.success) {
    throw new Error(data.error || 'Analysis failed');
  }
  return data.data;
};