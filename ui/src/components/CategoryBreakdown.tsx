
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CategoryTotal } from '@/types/transaction';
import { formatCurrency, getCategoryColor } from '@/utils/transactionUtils';

interface CategoryBreakdownProps {
  categories: CategoryTotal[];
}

const CategoryBreakdown: React.FC<CategoryBreakdownProps> = ({ categories }) => {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-medium">Spending by Category</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {categories.map((category) => (
            <div key={category.category} className="flex items-center">
              <div className={`w-3 h-3 rounded-full ${getCategoryColor(category.category)} mr-2`} />
              <div className="flex-1 flex justify-between items-center">
                <span className="capitalize">{category.category}</span>
                <span className="font-medium">{formatCurrency(category.total)}</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default CategoryBreakdown;
