import React, { useState } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';

const AssistantSection: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversation, setConversation] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    setConversation([...conversation, { role: 'user', content: question }]);
    setIsLoading(true);
    try {
      const response = await fetch('/api/assistant/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: question })
      });
      const data = await response.json();
      setConversation(prev => [...prev, { role: 'assistant', content: data.response || 'No response from assistant.' }]);
    } catch (err) {
      setConversation(prev => [...prev, { role: 'assistant', content: 'Error fetching assistant response.' }]);
    }
    setIsLoading(false);
    setQuestion('');
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg mb-10">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">Ask the Assistant</h3>
      </div>
      
      <div className="p-6">
        {conversation.length > 0 ? (
          <div className="mb-6 space-y-4 max-h-[300px] overflow-y-auto">
            {conversation.map((message, index) => (
              <div 
                key={index}
                className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
                    <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  </div>
                )}
                
                <div className={`px-4 py-3 rounded-lg max-w-[80%] ${
                  message.role === 'user' 
                    ? 'bg-blue-600 dark:bg-blue-700 text-white' 
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
                }`}>
                  <p className="text-sm">{message.content}</p>
                </div>
                
                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center flex-shrink-0">
                    <User className="h-5 w-5 text-gray-600 dark:text-gray-300" />
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
                  <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-700">
                  <Loader2 className="h-5 w-5 animate-spin text-gray-500 dark:text-gray-400" />
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-6 mb-6">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bot className="h-8 w-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h4 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Blockchain Assistant</h4>
            <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
              Ask questions about wallet analysis, blockchain security, or how to interpret the scoring results.
            </p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="relative">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question here..."
            className="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
          />
          <button
            type="submit"
            disabled={!question.trim() || isLoading}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>
        
        <div className="flex flex-wrap gap-2 justify-center mt-4 text-sm">
          {/* Example buttons removed */}
        </div>
      </div>
    </div>
  );
};

export default AssistantSection;