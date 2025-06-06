import React from 'react';
import { useWallet } from '../../contexts/WalletContext';

const activities = [
  {
    date: 'Today',
    events: [
      {
        type: 'transaction',
        time: '10:24 AM',
        description: 'Sent 0.5 ETH to 0x742...F3B2',
        highlight: false
      }
    ]
  },
  {
    date: 'Yesterday',
    events: [
      {
        type: 'contract',
        time: '3:45 PM',
        description: 'Interacted with Uniswap V3 contract',
        highlight: false
      },
      {
        type: 'transaction',
        time: '12:32 PM',
        description: 'Received 1,250 USDT from 0x381...A2E1',
        highlight: true
      }
    ]
  },
  {
    date: 'May 12, 2025',
    events: [
      {
        type: 'transaction',
        time: '7:14 PM',
        description: 'Sent 2.2 ETH to 0x912...B4C3',
        highlight: false
      },
      {
        type: 'contract',
        time: '5:30 PM',
        description: 'Approved USDC for Aave contract',
        highlight: false
      },
      {
        type: 'transaction',
        time: '2:45 PM',
        description: 'Received 4,500 USDC from 0x583...D1F2',
        highlight: false
      }
    ]
  }
];

const ActivityTimeline: React.FC = () => {
  const { walletData } = useWallet();
  
  if (!walletData) return null;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">Recent Activity</h3>
      </div>
      
      <div className="p-6 overflow-y-auto max-h-[400px] scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
        {activities.map((day, dayIndex) => (
          <div key={dayIndex} className={dayIndex > 0 ? 'mt-6' : ''}>
            <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">{day.date}</div>
            
            <div className="space-y-4">
              {day.events.map((event, eventIndex) => (
                <div key={eventIndex} className="relative pl-6">
                  {/* Timeline dot and line */}
                  <div className="absolute left-0 top-2 w-3 h-3 rounded-full bg-blue-500"></div>
                  {eventIndex < day.events.length - 1 && (
                    <div className="absolute left-1.5 top-4 w-0.5 h-full bg-gray-200 dark:bg-gray-700"></div>
                  )}
                  
                  <div className={`p-3 rounded-lg ${
                    event.highlight 
                      ? 'bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800' 
                      : 'bg-gray-50 dark:bg-gray-700/50'
                  }`}>
                    <div className="flex justify-between items-start mb-1">
                      <span className={`text-sm font-medium ${
                        event.highlight 
                          ? 'text-amber-800 dark:text-amber-300' 
                          : 'text-gray-900 dark:text-gray-100'
                      }`}>
                        {event.description}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">{event.time}</span>
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {event.type === 'transaction' ? 'Transaction' : 'Contract Interaction'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ActivityTimeline;