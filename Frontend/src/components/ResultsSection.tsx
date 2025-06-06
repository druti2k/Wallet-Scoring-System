import React from 'react';
import { useWallet } from '../contexts/WalletContext';
import ScoreOverview from './results/ScoreOverview';
import RiskMetrics from './results/RiskMetrics';
import TransactionHistory from './results/TransactionHistory';
import WalletInsights from './results/WalletInsights';
import ActivityTimeline from './results/ActivityTimeline';

const ResultsSection: React.FC = () => {
  const { walletData } = useWallet();

  if (!walletData) return null;

  return (
    <div className="mb-10 space-y-6 animate-in fade-in slide-in-from-bottom-5 duration-500">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Analysis Results</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <ScoreOverview />
        </div>
        <div className="lg:col-span-2">
          <RiskMetrics />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <WalletInsights />
        <ActivityTimeline />
      </div>
      
      <TransactionHistory />
    </div>
  );
};

export default ResultsSection;