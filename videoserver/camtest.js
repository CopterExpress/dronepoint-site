const rtsp = require('rtsp-ffmpeg');
const app = require('express')();
const cors = require('cors');

const isDev = process.argv.slice(2)[0] === 'dev';

require('dotenv').config({
  path: isDev ? '../.env' : '.'
});

app.use(cors());

const server = require('http').Server(app);
const io = require('socket.io')(server, { cors: { origin: '*' }});

const thermalParams = {
  resolution: '240x240',
  rate: 15,
  quality: 2,
  arguments: [
    '-reconnect', '1', 
    '-reconnect_streamed', '1',
    '-reconnect_delay_max', '2',
  ]
}

const camParams = {
  resolution: '720x576',
  rate: 15,
  quality: 1,
  arguments: [
    '-reconnect', '1', 
    '-reconnect_streamed', '1',
    '-reconnect_delay_max', '2',
  ]
}

const CONNECTION_URL = process.env.DRONE_CONNECTION || 'udpin:0.0.0.0:14550';

const stream = new rtsp.FFMpeg({ 
  ...camParams,
  input: `http://${CONNECTION_URL.split(':')[1]}:8080/stream?topic=/front_camera/image_raw`
})

const dpStream = new rtsp.FFMpeg({
  ...thermalParams,
  input: `http://${CONNECTION_URL.split(':')[1]}:8080/stream?topic=/thermal_camera/image_raw`,
})

const startStream = (streamObj, i) => {
  console.log(`Starting connection to ${CONNECTION_URL.split(':')[1]}`);
  streamObj.on('error', e => {
    console.log('Error in Stream');
  });
  streamObj.on('start', () => {
    console.log(`Stream ${i} started`);
  })
  streamObj.on('close', e => {
    console.log(`Stream ${i} closed`);
    // streamObj.start();
  });
  streamObj.on('data', () => {
      console.log(`receive data ${i}`);
  })
  streamObj.start();
}

const streams = Array(1000).fill(stream);

streams.forEach(startStream);

// io.on('connection', (socket) => {
//   console.log('connection');
//   const pipeStream = (data) => {
//     socket.emit('dronedata', data.toString('base64'))
//   }
//   const dpPipeStream = (data) => {
//     socket.emit('stationdata', data.toString('base64'));
//   }
//   stream.on('data', pipeStream);
//   dpStream.on('data', dpPipeStream);
//   socket.on('disconnect', () => {
//     stream.removeListener('data', pipeStream);
//     dpStream.removeListener('data', pipeStream);
//   });
// })

server.listen(5001, () => {
  console.log('Front test');
});