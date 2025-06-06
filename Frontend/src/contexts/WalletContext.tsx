import React, { createContext, useState, useContext } from 'react';
import { WalletData, NetworkType } from '../types/wallet';
import { analyzeWallet } from '../services/walletService';

interface WalletContextProps {
  walletAddress: string;
  setWalletAddress: (address: string) => void;
  walletData: WalletData | null;
  loading: boolean;
  error: string | null;
  selectedNetwork: NetworkType;
  setSelectedNetwork: (network: NetworkType) => void;
  analyzeWalletAddress: () => Promise<void>;
}

const WalletContext = createContext<WalletContextProps | undefined>(undefined);

export const WalletProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [walletAddress, setWalletAddress] = useState('');
  const [walletData, setWalletData] = useState<WalletData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedNetwork, setSelectedNetwork] = useState<NetworkType>('ethereum');

  const analyzeWalletAddress = async () => {
    if (!walletAddress.trim()) {
      setError('Please enter a wallet address');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await analyzeWallet(walletAddress, selectedNetwork);
      setWalletData(data);
    } catch (err) {
      setError('Failed to analyze wallet. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <WalletContext.Provider
      value={{
        walletAddress,
        setWalletAddress,
        walletData,
        loading,
        error,
        selectedNetwork,
        setSelectedNetwork,
        analyzeWalletAddress,
      }}
    >
      {children}
    </WalletContext.Provider>
  );
};

export const useWallet = (): WalletContextProps => {
  const context = useContext(WalletContext);
  if (!context) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
};