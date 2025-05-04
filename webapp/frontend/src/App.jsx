import React from 'react';
import { Filters } from './components/Filters';
import { Layout } from './components/Layout';
import { Charts } from './components/Charts';
import { useEffect } from 'react';
import { useState } from 'react';
import axios from 'axios';
import { API_URL } from './constants';

function App() {
  const [numberOfNodes, setNumberOfNodes] = useState(1);
  const [node, setNode] = useState(1);
  const [startTimeStamp, setStartTimestamp] = useState(null);
  const [endTimeStamp, setEndTimestamp] = useState(null);


  const changeNode = (node) => {
    setNode(node);
  }

  useEffect(() => {
    axios.get(`${API_URL}/node-count`)
      .then((response) => {
        setNumberOfNodes(response.data.nodeCount);
      })
      .catch((error) => {
        console.error('Error retrieving the number of nodes', error);
    });
  }, []);

  return (
    <div>
      <Layout
        title="Forest Protector"
        numberOfNodes={numberOfNodes}
        changeNode={changeNode}
        node={node}
      >
        <h1 style={{ marginBottom: '1.5rem'}} className='font-bold text-3xl p-4 px-10 rounded-2xl w-fit border border-black shadow-lg'>
          Data from node {node}
        </h1>
        <Filters
          startDateTime={startTimeStamp}
          setStartDateTime={setStartTimestamp}
          endDateTime={endTimeStamp}
          setEndDateTime={setEndTimestamp}
        />
        <Charts
          node={node}
          numberOfNodes={numberOfNodes}
          setNumberOfNodes={setNumberOfNodes}
          startTime={startTimeStamp}
          endTime={endTimeStamp}
        />
      </Layout>
    </div>
  );
}

export default App;
