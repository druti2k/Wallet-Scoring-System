import React from 'react';
import { ArrowUpRight, ArrowDownRight, BarChart3, Wallet } from 'lucide-react';
import { useWallet } from '../../contexts/WalletContext';

const WalletInsights: React.FC = () => {
  const { walletData } = useWallet();
  
  if (!walletData) return null;

  const insights = [
    {
      title: 'Total Value',
      value: '$42,839.25',
      change: '+5.2%',
      positive: true,
      icon: <Wallet className="h-5 w-5 text-purple-500" />
    },
    {
      title: 'Transactions',
      value: '246',
      change: '+12 this week',
      positive: true,
      icon: <BarChart3 className="h-5 w-5 text-blue-500" />
    },
    {
      title: 'Avg. Transaction',
      value: '$852.14',
      change: '-2.3%',
      positive: false,
      icon: <ArrowDownRight className="h-5 w-5 text-amber-500" />
    },
    {
      title: 'Active Since',
      value: '381 days',
      change: 'March 15, 2024',
      positive: true,
      icon: <ArrowUpRight className="h-5 w-5 text-green-500" />
    }
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">Wallet Insights</h3>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-2 gap-4">
          {insights.map((insight, index) => (
            <div 
              key={index}
              className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{insight.title}</span>
                <div className="p-2 rounded-full bg-gray-100 dark:bg-gray-700">
                  {insight.icon}
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold text-gray-900 dark:text-gray-100">{insight.value}</span>
                <span className={`text-xs ${insight.positive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                  {insight.change}
                </span>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-6 p-4 rounded-lg border border-blue-100 dark:border-blue-900 bg-blue-50 dark:bg-blue-900/20">
          <h4 className="font-medium text-blue-800 dark:text-blue-300 mb-2">Key Observation</h4>
          <p className="text-sm text-blue-700 dark:text-blue-400">
            This wallet shows regular transaction patterns consistent with normal trading activity. 
            The transaction frequency and value distribution suggest a long-term holder profile.
          </p>
        </div>
      </div>
    </div>
  );
};

export default WalletInsights;