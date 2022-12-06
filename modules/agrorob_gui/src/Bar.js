import React from 'react';
import { useState, useEffect } from 'react';
import mqtt from 'mqtt/dist/mqtt';
// import Card from '@mui/material/Card';
// import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { Button, CardActionArea, CardActions } from '@mui/material';
import Switch from '@mui/material/Switch';

const label = { inputProps: { 'aria-label': 'Switch demo' } };
// const options = {
//   clean: true,
//   clientId: 'clientId-ACywmtxjAM',
//   // username: 'babak',
//   // password: 'babak'
// };

// const client = mqtt.connect('ws:broker.hivemq.com:8000/mqtt');
// // connect to your cluster, insert your host name and port
// // const client = mqtt.connect('ws:broker.hivemq.com:8000/mqtt', options);


export default function Bar(){
//   const [connectionStatus, setConnectionStatus] = React.useState(false);
//   const [messages, setMessages] = React.useState([]);

//   useEffect(() => {
    
//     client.on('connect', () => setConnectionStatus(true));
//     client.on('message', (topic, payload, packet) => {
//       setMessages(messages.concat(payload.toString()));
//     });
//     client.subscribe('ros/topic/cmd_vel');
// // client.publish('messages', 'Hello, this message was received!');
//   }, []);

//   function handle(e) {
//     e.preventDefault();
//     client.publish('ros/bot/cms_vel', 'salam');
//   }


  return (
    <>
    <div style={{ 
      height: "400px",
      width: "400px",
      position: "absolute",
      top: "10px",
      right: "0px",
      zIndex: "2",
      margin: "20px",
      pointerEvents: "auto"}}>     
    <Card sx={{ maxWidth: 345 }}>
      <CardActionArea>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            Status
          </Typography>
          <Typography variant="body2" color="text.secondary">
           Connected
           <Box sx={{ display: 'flex' }}>
      <CircularProgress />
    </Box>
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button variant="contained" size="small" color="primary">
          Click
        </Button>
        <Switch {...label} defaultChecked />
      </CardActions>
    </Card>
      {/* {messages.map((message) => (
        <h2>{message}</h2>
     ))} */}
     
     {/* <Card variant="outlined">This is for your messages
      <Button variant="text">Text</Button>
      <Button variant="contained" color="success">Contained</Button>
      <Button variant="outlined" color="success">Outlined</Button></Card> */}
     </div>
     
    </>
  );
}