import React, { useState, useRef, useEffect } from 'react';
import { ArrowRightCircle, AlertTriangle, TrendingUp } from 'lucide-react';
import { useWallet } from '../../contexts/WalletContext';

const riskCategories = [
  { id: 'transaction', name: 'Transaction Patterns', score: 85 },
  { id: 'activity', name: 'Activity Consistency', score: 72 },
  { id: 'age', name: 'Wallet Age & History', score: 93 },
  { id: 'network', name: 'Network Interactions', score: 67 },
  { id: 'volume', name: 'Transaction Volumes', score: 78 },
  { id: 'mixing', name: 'Mixing Services Usage', score: 96 },
];

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

  if (!walletData) return null;

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div ref={animationRef} className="space-y-4">
            {riskCategories.map((category) => (
              <div key={category.id} className="risk-category opacity-0">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{category.name}</span>
                  <div className="flex items-center gap-1">
                    <span className={`text-sm font-bold ${getScoreColor(category.score)}`}>
                      {category.score}
                    </span>
                    {category.score < 70 && (
                      <AlertTriangle className="h-4 w-4 text-amber-500" />
                    )}
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
            <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <TrendingUp className="h-5 w-5 text-amber-500 mt-0.5" />
                <div>
                  <h4 className="font-medium text-amber-800 dark:text-amber-300">Unusual Activity Detected</h4>
                  <p className="text-sm text-amber-700 dark:text-amber-400 mt-1">
                    Transaction volume increased by 450% in the last 7 days compared to the previous 30-day average.
                  </p>
                </div>
              </div>
            </div>
            
            <h4 className="font-medium text-gray-900 dark:text-gray-100">Score History</h4>
            
            <div className="h-60 bg-white dark:bg-gray-800 rounded-lg p-4 flex items-end gap-2">
              {/* Simplified chart bars */}
              {[65, 72, 68, 75, 70, 82, 88].map((height, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div 
                    className="w-full bg-blue-500 dark:bg-blue-600 rounded-t-sm"
                    style={{ height: `${height}%` }}
                  ></div>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {i === 0 ? '7d' : i === 6 ? 'Now' : ''}
                  </span>
                </div>
              ))}
            </div>
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
        
        <div className="mt-6 text-right">
          <button className="inline-flex items-center text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
            Detailed risk analysis
            <ArrowRightCircle className="ml-1 h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RiskMetrics;