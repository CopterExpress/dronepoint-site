const rtsp = require('rtsp-ffmpeg');
const app = require('express')();
const cors = require('cors');
require('dotenv').config({ path: '../.env' });

app.use(cors());

const server = require('http').Server(app);
const io = require('socket.io')(server, { cors: { origin: '*' }});

const params = {
  resolution: '720x576',
  rate: 15,
}

const stream = new rtsp.FFMpeg({ 
  ...params,
  input: `http://${process.env.DRONE_CONNECTION.split(':')[1]}:8080/stream?topic=/front_camera/image_raw`
})

const dpStream = new rtsp.FFMpeg({
  ...params,
  input: `http://${process.env.DRONE_CONNECTION.split(':')[1]}:8080/stream?topic=/thermal_camera/image_raw`,
})

const startStream = (streamObj) => {
  streamObj.on('error', e => {
    console.log('Error in Stream');
  });
  streamObj.on('close', e => {
    console.log('Stream closed');
    streamObj.start();
  });
  streamObj.start();
}

const pipeStreams = (dronePipe, dpPipe) => {
  stream.on('data', dronePipe);
  dpStream.on('data', dpPipe);
}

startStream(stream);
startStream(dpStream);

io.on('connection', (socket) => {
  console.log('connection');
  const pipeStream = (data) => {
    console.log('sending drone');
    socket.emit('dronedata', data.toString('base64'))
  }
  const dpPipeStream = (data) => {
    console.log('sending station');
    socket.emit('stationdata', data.toString('base64'));
  }
  stream.on('data', pipeStream);
  dpStream.on('data', dpPipeStream);
  socket.on('disconnect', () => {
    stream.removeListener('data', pipeStream);
    dpStream.removeListener('data', pipeStream);
  });
})

server.listen(5001, () => {
  console.log('START SERVER');
});