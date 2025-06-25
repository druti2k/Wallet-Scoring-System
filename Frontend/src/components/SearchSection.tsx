import React, { useState } from 'react';
import { Search, ArrowRight, Loader2 } from 'lucide-react';
import { useWallet } from '../contexts/WalletContext';
import NetworkSelector from './NetworkSelector';

const SearchSection: React.FC = () => {
  const { walletAddress, setWalletAddress, analyzeWalletAddress, loading, error } = useWallet();
  const [hasFocused, setHasFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    analyzeWalletAddress();
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 mb-10 transform transition-all duration-500 hover:shadow-xl">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="flex flex-col md:flex-row items-stretch gap-4">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Enter wallet address"
              value={walletAddress}
              onChange={(e) => setWalletAddress(e.target.value)}
              onFocus={() => setHasFocused(true)}
              className={`block w-full pl-10 pr-4 py-3 border ${
                error && hasFocused ? 'border-red-300 dark:border-red-700' : 'border-gray-300 dark:border-gray-600'
              } rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all duration-200`}
            />
            {error && hasFocused && (
              <p className="mt-1 text-sm text-red-500 dark:text-red-400">{error}</p>
            )}
          </div>
          
          <NetworkSelector />
          
          <button
            type="submit"
            disabled={loading}
            className="flex items-center justify-center gap-2 py-3 px-6 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-medium rounded-lg transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed min-w-[120px]"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Analyzing</span>
              </>
            ) : (
              <>
                <span>Analyze</span>
                <ArrowRight className="h-5 w-5" />
              </>
            )}
          </button>
        </div>
        
        <div className="flex flex-wrap gap-2 justify-center text-sm text-gray-500 dark:text-gray-400">
          {/* Example buttons removed */}
        </div>
      </form>
    </div>
  );
};

export default SearchSection;