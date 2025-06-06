import React from 'react';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import { useWallet } from '../../contexts/WalletContext';

const ScoreOverview: React.FC = () => {
  const { walletData } = useWallet();
  
  if (!walletData) return null;
  
  const { score } = walletData;
  
  // Determine color and status based on score
  const getScoreInfo = () => {
    if (score >= 80) {
      return {
        color: 'text-green-500',
        bgColor: 'bg-green-100 dark:bg-green-900/20',
        icon: <CheckCircle className="h-8 w-8 text-green-500" />,
        status: 'Low Risk',
        description: 'This wallet shows normal behavior patterns consistent with legitimate usage.'
      };
    } else if (score >= 50) {
      return {
        color: 'text-amber-500',
        bgColor: 'bg-amber-100 dark:bg-amber-900/20',
        icon: <AlertTriangle className="h-8 w-8 text-amber-500" />,
        status: 'Medium Risk',
        description: 'Some suspicious patterns detected. Additional verification recommended.'
      };
    } else {
      return {
        color: 'text-red-500',
        bgColor: 'bg-red-100 dark:bg-red-900/20',
        icon: <Shield className="h-8 w-8 text-red-500" />,
        status: 'High Risk',
        description: 'Multiple red flags detected. Proceed with extreme caution when interacting with this wallet.'
      };
    }
  };
  
  const { color, bgColor, icon, status, description } = getScoreInfo();

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden h-full transition-all duration-300 hover:shadow-lg">
      <div className={`p-4 ${bgColor}`}>
        <div className="flex justify-between items-center">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">Trust Score</h3>
          <div className="flex items-center gap-1 text-sm font-medium text-gray-500 dark:text-gray-400">
            <span>Wallet</span>
            <span className="truncate max-w-[100px]">{walletData.address.substring(0, 6)}...{walletData.address.substring(walletData.address.length - 4)}</span>
          </div>
        </div>
      </div>
      
      <div className="p-6 flex flex-col items-center text-center">
        <div className="relative mb-4">
          <svg className="w-36 h-36" viewBox="0 0 100 100">
            <circle 
              className="text-gray-200 dark:text-gray-700" 
              strokeWidth="8" 
              stroke="currentColor" 
              fill="transparent" 
              r="40" 
              cx="50" 
              cy="50" 
            />
            <circle 
              className={color} 
              strokeWidth="8" 
              strokeDasharray={`${score * 2.51}, 251.2`}
              strokeLinecap="round" 
              stroke="currentColor" 
              fill="transparent" 
              r="40" 
              cx="50" 
              cy="50" 
              transform="rotate(-90 50 50)" 
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center flex-col">
            <span className={`text-4xl font-bold ${color}`}>{score}</span>
            <span className="text-gray-500 dark:text-gray-400 text-sm">out of 100</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2 mb-3">
          {icon}
          <span className={`font-bold ${color}`}>{status}</span>
        </div>
        
        <p className="text-gray-600 dark:text-gray-300 text-sm">{description}</p>
        
        <button className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors duration-200">
          View Detailed Report
        </button>
      </div>
    </div>
  );
};

export default ScoreOverview;