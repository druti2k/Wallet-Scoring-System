import React, { useState } from 'react';
import { ArrowDownRight, ArrowUpRight, FileText, ExternalLink } from 'lucide-react';
import { useWallet } from '../../contexts/WalletContext';

const transactions = [
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
  {
    id: 'tx3',
    hash: '0x3d5c9b57a8a954e4f792df362af8d64f770d8e6ecaf12b53c3413930f338e19a',
    type: 'outgoing',
    amount: '2.2 ETH',
    value: '$5,435.84',
    to: '0x912e...B4C3',
    from: '0x3a1b...C5D2',
    timestamp: '2025-05-12T19:14:00Z',
    gas: '0.0025 ETH'
  },
  {
    id: 'tx4',
    hash: '0x9e7c1a37eef8c9e4e6a4e6c8d2c8e8a3d8c1e8c1a37eef8c9e4e6a4e6c8d2c8e',
    type: 'incoming',
    amount: '4,500 USDC',
    value: '$4,500.00',
    to: '0x3a1b...C5D2',
    from: '0x583f...D1F2',
    timestamp: '2025-05-12T14:45:00Z',
    gas: '0.0017 ETH'
  }
];

const TransactionHistory: React.FC = () => {
  const { walletData } = useWallet();
  const [visibleDetails, setVisibleDetails] = useState<string | null>(null);
  
  if (!walletData) return null;

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