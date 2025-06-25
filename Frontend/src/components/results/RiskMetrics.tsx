import React, { useState, useRef, useEffect } from 'react';
import { ArrowRightCircle, AlertTriangle, TrendingUp } from 'lucide-react';
import { useWallet } from '../../contexts/WalletContext';

const RiskMetrics: React.FC = () => {
  const { walletData } = useWallet();
  const [activeTab, setActiveTab] = useState('overview');
  const animationRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    if (animationRef.current) {
      const categories = animationRef.current.querySelectorAll('.risk-category');
      categories.forEach((category, index) => {
        setTimeout(() => {
          category.classList.add('animate-in', 'fade-in', 'slide-in-from-bottom-3');
        }, index * 100);
      });
    }
  }, []);

  if (!walletData || !Array.isArray(walletData.metrics)) return null;
  const metrics = walletData.metrics || [];
  if (metrics.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden h-full transition-all duration-300 hover:shadow-lg p-6 text-center text-gray-500 dark:text-gray-400">
        No risk metrics found for this wallet.
      </div>
    );
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div ref={animationRef} className="space-y-4">
            {metrics.map((category) => (
              <div key={category.id} className="risk-category opacity-0">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{category.name}</span>
                  <div className="flex items-center gap-1">
                    <span className={`text-sm font-bold ${getScoreColor(category.score)}`}>
                      {category.score}
                    </span>
                  </div>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getScoreBackgroundColor(category.score)}`}
                    style={{ width: `${category.score}%`, transition: 'width 1s ease-in-out' }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        );
      case 'history':
        return (
          <div className="space-y-4 animate-in fade-in duration-300">
            <div className="text-gray-500 dark:text-gray-400 text-center">No score history available.</div>
          </div>
        );
      default:
        return null;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-amber-600 dark:text-amber-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBackgroundColor = (score: number) => {
    if (score >= 80) return 'bg-green-500 dark:bg-green-400';
    if (score >= 60) return 'bg-amber-500 dark:bg-amber-400';
    return 'bg-red-500 dark:bg-red-400';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden h-full transition-all duration-300 hover:shadow-lg">
      <div className="border-b border-gray-200 dark:border-gray-700">
        <div className="flex">
          <button
            className={`px-4 py-3 font-medium text-sm focus:outline-none ${
              activeTab === 'overview'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
            onClick={() => setActiveTab('overview')}
          >
            Risk Overview
          </button>
          <button
            className={`px-4 py-3 font-medium text-sm focus:outline-none ${
              activeTab === 'history'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            }`}
            onClick={() => setActiveTab('history')}
          >
            Score History
          </button>
        </div>
      </div>
      
      <div className="p-6">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default RiskMetrics;