
import React from 'react';
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { BarChart3, PieChart } from "lucide-react";

interface ChartToggleProps {
  activeChart: 'pie' | 'bar';
  onChange: (value: 'pie' | 'bar') => void;
}

const ChartToggle: React.FC<ChartToggleProps> = ({ activeChart, onChange }) => {
  return (
    <ToggleGroup type="single" value={activeChart} onValueChange={(value) => value && onChange(value as 'pie' | 'bar')}>
      <ToggleGroupItem value="bar" aria-label="Bar Chart">
        <BarChart3 className="h-4 w-4" />
      </ToggleGroupItem>
      <ToggleGroupItem value="pie" aria-label="Pie Chart">
        <PieChart className="h-4 w-4" />
      </ToggleGroupItem>
    </ToggleGroup>
  );
};

export default ChartToggle;
