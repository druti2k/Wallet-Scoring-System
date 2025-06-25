import React, { useState } from 'react';
import { ArrowDownRight, ArrowUpRight, FileText, ExternalLink } from 'lucide-react';
import { useWallet } from '../../contexts/WalletContext';

const TransactionHistory: React.FC = () => {
  const { walletData } = useWallet();
  const [visibleDetails, setVisibleDetails] = useState<string | null>(null);
  
  if (!walletData || !Array.isArray(walletData.recentTransactions)) return null;
  const transactions = walletData.recentTransactions || [];
  if (transactions.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg p-6 text-center text-gray-500 dark:text-gray-400">
        No transactions found for this wallet.
      </div>
    );
  }

  const toggleDetails = (id: string) => {
    if (visibleDetails === id) {
      setVisibleDetails(null);
    } else {
      setVisibleDetails(id);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    });
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">Transaction History</h3>
        <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline">View All</button>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-700/50 text-left">
            <tr>
              <th className="px-6 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Transaction</th>
              <th className="px-6 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Value</th>
              <th className="px-6 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">From/To</th>
              <th className="px-6 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {transactions.map((tx) => (
              <React.Fragment key={tx.id}>
                <tr className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-150">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        tx.type === 'incoming' 
                          ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' 
                          : 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
                      }`}>
                        {tx.type === 'incoming' ? <ArrowDownRight className="h-5 w-5" /> : <ArrowUpRight className="h-5 w-5" />}
                      </div>
                      <div className="ml-3">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {tx.type === 'incoming' ? 'Received' : 'Sent'} {tx.amount}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {tx.hash.substring(0, 7)}...{tx.hash.substring(tx.hash.length - 5)}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900 dark:text-gray-100">{tx.value}</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Gas: {tx.gas}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900 dark:text-gray-100">
                      {tx.type === 'incoming' ? 'From: ' : 'To: '}
                      <span className="font-medium">
                        {tx.type === 'incoming' ? tx.from : tx.to}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-100">
                    {formatDate(tx.timestamp)}
                  </td>
                  <td className="px-6 py-4 text-right text-sm">
                    <button 
                      onClick={() => toggleDetails(tx.id)}
                      className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mr-3"
                    >
                      <FileText className="h-5 w-5" />
                    </button>
                    <a 
                      href={`https://etherscan.io/tx/${tx.hash}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
                    >
                      <ExternalLink className="h-5 w-5" />
                    </a>
                  </td>
                </tr>
                
                {/* Expanded details row */}
                {visibleDetails === tx.id && (
                  <tr className="bg-gray-50 dark:bg-gray-700/30">
                    <td colSpan={5} className="px-6 py-4">
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <div className="text-gray-500 dark:text-gray-400 font-medium">Transaction Hash</div>
                          <div className="text-gray-900 dark:text-gray-100 truncate">{tx.hash}</div>
                        </div>
                        <div>
                          <div className="text-gray-500 dark:text-gray-400 font-medium">From</div>
                          <div className="text-gray-900 dark:text-gray-100">{tx.from}</div>
                        </div>
                        <div>
                          <div className="text-gray-500 dark:text-gray-400 font-medium">To</div>
                          <div className="text-gray-900 dark:text-gray-100">{tx.to}</div>
                        </div>
                        <div>
                          <div className="text-gray-500 dark:text-gray-400 font-medium">Status</div>
                          <div className="text-green-600 dark:text-green-400">Confirmed</div>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionHistory;