import { Chart } from './Chart';
import { useData } from '../../hooks/useData';
import { Stack, Skeleton } from '@mui/material';

import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';
import { NoData } from '../NoData';

const Item = styled(Paper)(({ theme }) => ({
	backgroundColor: '#fff',
	...theme.typography.body2,
	padding: theme.spacing(1),
	textAlign: 'center',
	color: theme.palette.text.secondary,
	flexGrow: 1,
	...theme.applyStyles('dark', {
		backgroundColor: '#1A2027',
	}),
}));

function ChartSkeletons({ numberofskeletons }) {
	return (
		<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
			{Array.from(new Array(numberofskeletons)).map((_, index) => (
				<Skeleton key={index} variant="rectangular" width="100%" height={400} />
			))}
		</div>
	);
}

export function Charts({ node, numberOfNodes, setNumberOfNodes, startTime = null, endTime = null }) {
	const { data, loading, error } = useData({ node, startTime, endTime, numberOfNodes, setNumberOfNodes });

	const fields = data ? (data.y)
		.filter((item) => item.name !== 'node' && item.name !== 'timestamp' && item.name !== '_id')
		.map((item) => item.name) : [];

	const x = data
		? data.x.data
		: [];
	const y = data
		? (field) => data.y
			.filter((item) => item.name === field)[0].data
			.map(value => typeof value === 'boolean' ? (value ? 1 : 0) : value)
			.map(value => parseFloat(value))
		: [];

	return (
		<div style={{ marginTop: "5vh" }}>
			{loading && <ChartSkeletons numberofskeletons={fields.length} />}
			{error && <div>{error}</div>}
			{!loading && !error && data && (
				<div
					className="grid grid-cols-1 md:grid-cols-2 gap-4"
				>
					{fields.map((field, index) => (
						<Chart
							x={x}
							y={y(field)}
							name={field}
							key={index}
						/>
					))}
				</div>
			)}
			{!loading && !error && !data && (
				<NoData >
					{ (startTime || endTime) ? 'No data found for the selected time range' : 'No data found' }
				</NoData>
			)}
		</div>
	);
};
