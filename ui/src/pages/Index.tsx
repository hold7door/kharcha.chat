
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { mockTransactions } from '@/data/mockTransactions';
import { calculateCategoryTotals, calculateTotalBalance } from '@/utils/transactionUtils';
import CategoryPieChart from '@/components/CategoryPieChart';
import SpendingBarChart from '@/components/SpendingBarChart';
import CategoryBreakdown from '@/components/CategoryBreakdown';
import TransactionList from '@/components/TransactionList';
import BalanceCard from '@/components/BalanceCard';
import ChartToggle from '@/components/ChartToggle';

const Index = () => {
  const [activeChart, setActiveChart] = useState<'pie' | 'bar'>('pie');
  
  const categoryTotals = calculateCategoryTotals(mockTransactions);
  const totalBalance = calculateTotalBalance(mockTransactions);
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <div className="flex flex-col space-y-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Budget Glimpse</h1>
            <p className="text-muted-foreground mt-1">Visualize your spending across categories</p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-4">
            <div className="md:col-span-3">
              <Card className="h-full">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <div className="space-y-1">
                    <CardTitle className="text-lg font-medium">Spending Analysis</CardTitle>
                    <CardDescription>Visual breakdown of your spending by category</CardDescription>
                  </div>
                  <ChartToggle activeChart={activeChart} onChange={setActiveChart} />
                </CardHeader>
                <CardContent>
                  {activeChart === 'pie' ? (
                    <CategoryPieChart data={categoryTotals} />
                  ) : (
                    <SpendingBarChart data={categoryTotals} />
                  )}
                </CardContent>
              </Card>
            </div>
            
            <div>
              <div className="grid gap-6">
                <BalanceCard balance={totalBalance} />
                <CategoryBreakdown categories={categoryTotals} />
              </div>
            </div>
          </div>
          
          <TransactionList transactions={mockTransactions} />
        </div>
      </div>
    </div>
  );
};

export default Index;
