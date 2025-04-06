
export type TransactionType = 'debit' | 'credit';

export interface Transaction {
  id: string;
  date: string;
  category: string;
  description: string;
  amount: number;
  type: TransactionType;
}

export interface CategoryTotal {
  category: string;
  total: number;
  percentage: number;
}
