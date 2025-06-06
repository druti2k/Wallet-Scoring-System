import React from 'react';
import Navbar from './Navbar';
import Header from './Header';
import SearchSection from './SearchSection';
import ResultsSection from './ResultsSection';
import AssistantSection from './AssistantSection';
import Footer from './Footer';
import { useWallet } from '../contexts/WalletContext';

const Layout: React.FC = () => {
  const { walletData } = useWallet();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
      <Navbar />
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <Header />
        <SearchSection />
        {walletData && <ResultsSection />}
        <AssistantSection />
      </main>
      <Footer />
    </div>
  );
};

export default Layout;