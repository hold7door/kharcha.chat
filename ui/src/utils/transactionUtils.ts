
import { Transaction, CategoryTotal } from "@/types/transaction";

export function calculateCategoryTotals(transactions: Transaction[]): CategoryTotal[] {
  // Only consider debit transactions for spending analysis
  const debits = transactions.filter(transaction => transaction.type === 'debit');
  
  // Calculate total debits
  const totalSpent = debits.reduce((sum, transaction) => sum + transaction.amount, 0);
  
  // Group transactions by category and calculate totals
  const categoryMap = new Map<string, number>();
  
  debits.forEach(transaction => {
    const currentTotal = categoryMap.get(transaction.category) || 0;
    categoryMap.set(transaction.category, currentTotal + transaction.amount);
  });
  
  // Convert to array and calculate percentages
  const categoryTotals: CategoryTotal[] = Array.from(categoryMap.entries()).map(([category, total]) => {
    return {
      category,
      total,
      percentage: (total / totalSpent) * 100
    };
  });
  
  // Sort by total amount (descending)
  return categoryTotals.sort((a, b) => b.total - a.total);
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'INR',
  }).format(amount);
}

export function getTransactionTypeColor(type: 'debit' | 'credit'): string {
  return type === 'debit' ? 'text-red-500' : 'text-green-500';
}

export function getCategoryColor(category: string): string {
  const colorMap: Record<string, string> = {
    food: 'bg-chart-food',
    shopping: 'bg-chart-shopping',
    transport: 'bg-chart-transport',
    utilities: 'bg-chart-utilities',
    entertainment: 'bg-chart-entertainment',
    health: 'bg-chart-health',
    education: 'bg-chart-education',
    other: 'bg-chart-other',
  };
  
  return colorMap[category] || 'bg-gray-400';
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
}

export function calculateTotalBalance(transactions: Transaction[]): number {
  return transactions.reduce((balance, transaction) => {
    if (transaction.type === 'credit') {
      return balance + transaction.amount;
    } else {
      return balance - transaction.amount;
    }
  }, 0);
}
