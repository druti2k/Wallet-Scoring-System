import React from 'react';
import { ChevronDown } from 'lucide-react';
import { useWallet } from '../contexts/WalletContext';
import { NetworkType } from '../types/wallet';

const networkOptions: { value: NetworkType; label: string; icon: string }[] = [
  { value: 'ethereum', label: 'Ethereum', icon: '🔷' },
  { value: 'bitcoin', label: 'Bitcoin', icon: '₿' },
  { value: 'solana', label: 'Solana', icon: '◎' },
  { value: 'polygon', label: 'Polygon', icon: '⬡' },
  { value: 'binance', label: 'BNB Chain', icon: '🟨' },
];

const NetworkSelector: React.FC = () => {
  const { selectedNetwork, setSelectedNetwork } = useWallet();
  const [isOpen, setIsOpen] = React.useState(false);

  const selectedOption = networkOptions.find(option => option.value === selectedNetwork);

  return (
    <div className="relative min-w-[180px]">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all duration-200"
      >
        <div className="flex items-center gap-2">
          <span className="text-lg">{selectedOption?.icon}</span>
          <span>{selectedOption?.label}</span>
        </div>
        <ChevronDown className={`h-5 w-5 text-gray-500 transition-transform duration-200 ${isOpen ? 'transform rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 animate-in fade-in slide-in-from-top-5 duration-200">
          {networkOptions.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => {
                setSelectedNetwork(option.value);
                setIsOpen(false);
              }}
              className={`flex items-center gap-2 w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${
                selectedNetwork === option.value 
                  ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                  : 'text-gray-900 dark:text-gray-100'
              }`}
            >
              <span className="text-lg">{option.icon}</span>
              <span>{option.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default NetworkSelector;