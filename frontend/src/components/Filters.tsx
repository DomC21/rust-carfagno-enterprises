import { Calendar as CalendarIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Calendar } from "@/components/ui/calendar"
import { DateRange } from "react-day-picker"

interface FiltersProps {
  onFilterChange: (filters: {
    startDate?: Date
    endDate?: Date
    publisher?: string
    sentiment?: string
  }) => void
}

export function Filters({ onFilterChange }: FiltersProps): JSX.Element {
  return (
    <div className="flex flex-wrap gap-4 mb-6">
      <div className="flex gap-2">
        <Popover>
          <PopoverTrigger asChild>
            <Button variant="outline" className="text-primary">
              <CalendarIcon className="mr-2" size={20} />
              Date Range
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0 bg-popover" align="start">
            <Calendar
              mode="range"
              className="border-0"
              onSelect={(range: DateRange | undefined) => {
                if (range?.from && range?.to) {
                  onFilterChange({
                    startDate: range.from,
                    endDate: range.to,
                  })
                }
              }}
            />
          </PopoverContent>
        </Popover>
      </div>

      <Select
        onValueChange={(value) =>
          onFilterChange({
            publisher: value === "all" ? undefined : value,
          })
        }
      >
        <SelectTrigger className="w-[180px] bg-popover text-foreground border-border">
          <SelectValue placeholder="Publisher" />
        </SelectTrigger>
        <SelectContent className="bg-popover text-foreground border-border">
          <SelectItem value="all">All Publishers</SelectItem>
          <SelectItem value="reuters">Reuters</SelectItem>
          <SelectItem value="bloomberg">Bloomberg</SelectItem>
          <SelectItem value="wsj">Wall Street Journal</SelectItem>
        </SelectContent>
      </Select>

      <Select
        onValueChange={(value) =>
          onFilterChange({
            sentiment: value === "all" ? undefined : value,
          })
        }
      >
        <SelectTrigger className="w-[180px] bg-popover text-foreground border-border">
          <SelectValue placeholder="Sentiment" />
        </SelectTrigger>
        <SelectContent className="bg-popover text-foreground border-border">
          <SelectItem value="all">All Sentiments</SelectItem>
          <SelectItem value="positive">Positive</SelectItem>
          <SelectItem value="neutral">Neutral</SelectItem>
          <SelectItem value="negative">Negative</SelectItem>
        </SelectContent>
      </Select>
    </div>
  )
}
