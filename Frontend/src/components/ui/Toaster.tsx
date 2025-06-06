import React, { useState, useEffect, createContext, useContext } from 'react';
import { X, AlertCircle, CheckCircle, Info } from 'lucide-react';

type ToastType = 'success' | 'error' | 'info';

interface Toast {
  id: string;
  message: string;
  type: ToastType;
}

interface ToasterContextProps {
  addToast: (message: string, type: ToastType) => void;
  removeToast: (id: string) => void;
}

const ToasterContext = createContext<ToasterContextProps | undefined>(undefined);

export const useToaster = (): ToasterContextProps => {
  const context = useContext(ToasterContext);
  if (!context) {
    throw new Error('useToaster must be used within a ToasterProvider');
  }
  return context;
};

export const ToasterProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (message: string, type: ToastType) => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  return (
    <ToasterContext.Provider value={{ addToast, removeToast }}>
      {children}
      <Toaster toasts={toasts} removeToast={removeToast} />
    </ToasterContext.Provider>
  );
};

interface ToasterProps {
  toasts: Toast[];
  removeToast: (id: string) => void;
}

export const Toaster: React.FC<ToasterProps> = ({ toasts = [], removeToast }) => {
  return (
    <div className="fixed bottom-0 right-0 p-4 space-y-2 z-50 max-w-sm w-full">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} removeToast={removeToast} />
      ))}
    </div>
  );
};

interface ToastItemProps {
  toast: Toast;
  removeToast: (id: string) => void;
}

const ToastItem: React.FC<ToastItemProps> = ({ toast, removeToast }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      removeToast(toast.id);
    }, 5000);

    return () => clearTimeout(timer);
  }, [toast.id, removeToast]);

  const getIcon = () => {
    switch (toast.type) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case 'info':
        return <Info className="h-5 w-5 text-blue-500" />;
      default:
        return null;
    }
  };

  const getBgColor = () => {
    switch (toast.type) {
      case 'success':
        return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800';
      case 'error':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800';
      case 'info':
        return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800';
      default:
        return 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700';
    }
  };

  return (
    <div 
      className={`${getBgColor()} border rounded-lg shadow-lg p-4 transform transition-all duration-300 ease-in-out animate-in fade-in slide-in-from-bottom-5`}
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          {getIcon()}
        </div>
        <div className="ml-3 flex-1">
          <p className="text-sm text-gray-800 dark:text-gray-200">{toast.message}</p>
        </div>
        <button
          onClick={() => removeToast(toast.id)}
          className="ml-4 text-gray-400 hover:text-gray-500 focus:outline-none"
        >
          <X className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

export default Toaster;