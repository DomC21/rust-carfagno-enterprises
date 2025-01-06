import React from 'react';
import { Button } from './ui/button';
import { Calendar } from './ui/calendar';
import { format } from 'date-fns';

interface FiltersProps {
  onDateChange: (startDate: Date | undefined, endDate: Date | undefined) => void;
  onReset: () => void;
}

const Filters: React.FC<FiltersProps> = ({ onDateChange, onReset }) => {
  const [startDate, setStartDate] = React.useState<Date>();
  const [endDate, setEndDate] = React.useState<Date>();

  const handleDateChange = (date: Date | undefined, isStart: boolean) => {
    if (isStart) {
      setStartDate(date);
      onDateChange(date, endDate);
    } else {
      setEndDate(date);
      onDateChange(startDate, date);
    }
  };

  const handleReset = () => {
    setStartDate(undefined);
    setEndDate(undefined);
    onReset();
  };

  return (
    <div className="space-y-4 p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold">Filters</h3>
      
      <div className="space-y-2">
        <label className="block text-sm font-medium">Date Range</label>
        <div className="flex gap-4">
          <div>
            <span className="text-sm text-gray-500">Start Date</span>
            <Calendar
              mode="single"
              selected={startDate}
              onSelect={(date) => handleDateChange(date, true)}
              className="rounded-md border"
            />
          </div>
          <div>
            <span className="text-sm text-gray-500">End Date</span>
            <Calendar
              mode="single"
              selected={endDate}
              onSelect={(date) => handleDateChange(date, false)}
              className="rounded-md border"
            />
          </div>
        </div>
      </div>

      <Button onClick={handleReset} variant="outline" className="w-full">
        Reset Filters
      </Button>
    </div>
  );
};

export default Filters;
