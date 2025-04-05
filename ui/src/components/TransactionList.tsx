
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Transaction } from '@/types/transaction';
import { formatCurrency, formatDate, getTransactionTypeColor } from '@/utils/transactionUtils';

interface TransactionListProps {
  transactions: Transaction[];
}

const TransactionList: React.FC<TransactionListProps> = ({ transactions }) => {
  const sortedTransactions = [...transactions].sort((a, b) => 
    new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-medium">Recent Transactions</CardTitle>
      </CardHeader>
      <CardContent className="px-0">
        <div className="space-y-1">
          {sortedTransactions.slice(0, 7).map((transaction) => (
            <div 
              key={transaction.id}
              className="flex items-center justify-between py-2 px-6 hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center space-x-4">
                <div className={`w-2 h-2 rounded-full ${getTransactionTypeColor(transaction.type)}`} />
                <div>
                  <p className="font-medium text-sm">{transaction.description}</p>
                  <p className="text-xs text-muted-foreground capitalize">
                    {transaction.category} • {formatDate(transaction.date)}
                  </p>
                </div>
              </div>
              <div className={`font-medium ${transaction.type === 'credit' ? 'text-green-500' : ''}`}>
                {transaction.type === 'credit' ? '+' : ''}{formatCurrency(transaction.amount)}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default TransactionList;
