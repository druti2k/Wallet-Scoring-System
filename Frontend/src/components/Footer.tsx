import React from 'react';
import { Shield, Github, Twitter } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-t border-gray-200 dark:border-gray-700 transition-colors duration-300 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex flex-col items-center justify-center">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-8 h-8 bg-blue-600 dark:bg-blue-500 rounded-md flex items-center justify-center">
              <Shield className="h-5 w-5 text-white" />
            </div>
            <span className="text-blue-600 dark:text-blue-400 font-bold text-xl">BlockScan</span>
          </div>
          <p className="text-gray-600 dark:text-gray-300 text-sm mb-2">Advanced blockchain analytics platform.</p>
        </div>
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 text-center text-sm text-gray-500 dark:text-gray-400">
          © {new Date().getFullYear()} BlockScan. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;