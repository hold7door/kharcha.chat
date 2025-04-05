
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { CategoryTotal } from '@/types/transaction';
import { formatCurrency, getCategoryColor } from '@/utils/transactionUtils';

interface CategoryPieChartProps {
  data: CategoryTotal[];
}

const CategoryPieChart: React.FC<CategoryPieChartProps> = ({ data }) => {
  // Prepare data for the pie chart
  const chartData = data.map(item => ({
    name: item.category.charAt(0).toUpperCase() + item.category.slice(1),
    value: item.total,
    color: getCategoryColor(item.category).replace('bg-', ''),
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-2 shadow rounded border">
          <p className="text-sm font-medium">{payload[0].name}</p>
          <p className="text-sm">{formatCurrency(payload[0].value)}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={2}
            dataKey="value"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            labelLine={false}
          >
            {chartData.map((entry, index) => {
              const colorClass = `chart-${entry.color.split('-').pop()}`;
              return (
                <Cell 
                  key={`cell-${index}`} 
                  fill={`var(--${colorClass}, #94a3b8)`} // Fallback to slate-400
                />
              );
            })}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CategoryPieChart;
