FROM node:12

WORKDIR .

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5001

CMD [ "node", "videoserver.js" ]