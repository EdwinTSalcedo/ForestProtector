import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

// xData must be a time series. Example: ['2021-01-01T00:00:00Z', '2021-01-01T00:01:00Z', ...]
// yData must be a list of numbers. Example: [1, 2, 3, ... ...]

export function Chart({ x = [], y = [], name = 'value' }) {

  // Sort the data by timestamp
  const combinedData = x.map((xData, index) => ({ x: xData, y: y[index] }));
  combinedData.sort((a, b) => new Date(a.x) - new Date(b.x));
  x = combinedData.map(data => data.x);
  y = combinedData.map(data => data.y);

  const data = x.map((xData, index) => {
    const date = new Date(xData);
    return {
      hour: `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`,
      [name]: parseFloat(y[index]),
    };
  });

  return (
    <div>
      <h1
        style={{
          textAlign: 'center',
          fontSize: '1.5rem',
          marginBottom: '1rem',
          textTransform: 'uppercase',
        }}
      >
        {name}
      </h1>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="hour" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey={name} stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
