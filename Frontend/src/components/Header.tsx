import React from 'react';
import { Shield, ShieldCheck, ShieldAlert } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <div className="mb-12 text-center">
      <div className="inline-flex items-center justify-center p-1 mb-4 bg-blue-100 dark:bg-blue-900/30 rounded-full text-blue-800 dark:text-blue-300">
        <span className="px-3 py-1 text-xs font-medium">Advanced Blockchain Analytics</span>
      </div>
      <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-teal-500 dark:from-blue-400 dark:to-teal-300">
        Behavioral Wallet Scoring System
      </h1>
      <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
        Analyze blockchain wallets for risk assessment, behavioral patterns, and security insights using advanced AI algorithms.
      </p>
      
      <div className="flex flex-wrap justify-center gap-6 mt-8">
        <div className="flex items-center gap-2 bg-white dark:bg-gray-800 rounded-full px-4 py-2 shadow-sm">
          <ShieldCheck className="text-green-500" size={20} />
          <span className="text-sm text-gray-700 dark:text-gray-200">Security Focused</span>
        </div>
        <div className="flex items-center gap-2 bg-white dark:bg-gray-800 rounded-full px-4 py-2 shadow-sm">
          <Shield className="text-blue-500" size={20} />
          <span className="text-sm text-gray-700 dark:text-gray-200">Multi-Network Support</span>
        </div>
        <div className="flex items-center gap-2 bg-white dark:bg-gray-800 rounded-full px-4 py-2 shadow-sm">
          <ShieldAlert className="text-amber-500" size={20} />
          <span className="text-sm text-gray-700 dark:text-gray-200">Risk Detection</span>
        </div>
      </div>
    </div>
  );
};

export default Header;