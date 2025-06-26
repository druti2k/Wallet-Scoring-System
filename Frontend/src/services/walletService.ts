import { WalletData, NetworkType } from '../types/wallet';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');

// Service to connect to the real backend API for wallet analysis

export const analyzeWallet = async (address: string, network: NetworkType): Promise<WalletData> => {
  const response = await fetch(`${API_BASE_URL}/api/wallet/${address}?network=${network}`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    console.error('API Error:', errorData);
    throw new Error(errorData.detail || 'Failed to fetch wallet analysis');
  }
  const data = await response.json();
  console.log('API response:', data); // Debugging line
  if (!data.success) {
    throw new Error(data.error || 'Analysis failed');
  }
  return data.data;
};