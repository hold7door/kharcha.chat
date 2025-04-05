
export type TransactionType = 'debit' | 'credit';

export type TransactionCategory =
  | 'food'
  | 'shopping'
  | 'transport'
  | 'utilities'
  | 'entertainment'
  | 'health'
  | 'education'
  | 'other';

export interface Transaction {
  id: string;
  date: string;
  category: TransactionCategory;
  description: string;
  amount: number;
  type: TransactionType;
}

export interface CategoryTotal {
  category: TransactionCategory;
  total: number;
  percentage: number;
}
