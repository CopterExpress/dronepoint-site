const rtsp = require('rtsp-ffmpeg');
const app = require('express')();
const cors = require('cors');

app.use(cors());

const server = require('http').Server(app);
const io = require('socket.io')(server, { cors: { origin: '*' }});

const stream = new rtsp.FFMpeg({ 
  input: 'http://192.168.194.207:8080/stream?topic=/main_camera/image_raw'
})

const dpStream = new rtsp.FFMpeg({
  input: 'http://192.168.194.183:8080/stream?topic=/main_camera/image_raw',
})

dpStream.on('data', e => {
  // console.log("YEEEEE");
});

dpStream.on('error', e => {
  console.log('error dp');
  console.log(e);
})

dpStream.on('close', e => {
  console.log('close dp');
  console.log(e);
})

stream.on('error', e => {
  console.log('error');
  console.log(e);
})

stream.on('close', e => {
  console.log('close');
  console.log(e);
})

stream.on('data', e => {
  // console.log('drone data');
})

stream.start();

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
  });
})

server.listen(5001, () => {
  console.log('START SERVER');
});