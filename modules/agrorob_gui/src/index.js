import React from 'react';
import { render} from 'react-dom';
import MapLoader from './MapLoader';
import Bar from './Bar';
import mqtt from 'mqtt/dist/mqtt';

// Render the application

const root = document.querySelector('#root');
render((<>
<MapLoader></MapLoader>
        <Bar></Bar></>), root)