FROM node:12

RUN apt-get -y update

RUN apt-get install -y ffmpeg

WORKDIR .

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5001

CMD node videoStream.js prod