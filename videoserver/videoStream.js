const rtsp = require('rtsp-ffmpeg');
const app = require('express')();
const cors = require('cors');

app.use(cors());

const server = require('http').Server(app);
const io = require('socket.io')(server, { cors: { origin: '*' }});

const stream = new rtsp.FFMpeg({ 
  input: 'http://190.0.0.182:8080/stream?topic=/front_camera/image_raw'
})

const dpStream = new rtsp.FFMpeg({
  input: 'http://190.0.0.182:8080/stream?topic=/thermal_camera/image_raw',
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