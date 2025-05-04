import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';



export function Filters({ startDateTime, setStartDateTime, endDateTime, setEndDateTime }) {
  return (
    <div>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DemoContainer components={['DateTimePicker']}>
          <div className='flex justify-center gap-2'>
            <DateTimePicker label="Start TimeStamp" value={startDateTime} onChange={setStartDateTime} />
            <DateTimePicker label="End TimeStamp" value={endDateTime} onChange={setEndDateTime} />
          </div>
        </DemoContainer>
      </LocalizationProvider>
    </div>
  );
}