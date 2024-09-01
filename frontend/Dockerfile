FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN ls -al

RUN npm install

COPY . .

RUN ls -al

RUN npm run build

CMD ["npm", "run", "preview"]

EXPOSE 3000