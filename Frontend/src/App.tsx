import { ThemeProvider } from './contexts/ThemeContext';
import { WalletProvider } from './contexts/WalletContext';
import Layout from './components/Layout';
import { Toaster } from './components/ui/Toaster';

function App() {
  return (
    <ThemeProvider>
      <WalletProvider>
        <Layout />
        <Toaster toasts={[]} removeToast={() => {}} />
      </WalletProvider>
    </ThemeProvider>
  );
}


export default App;