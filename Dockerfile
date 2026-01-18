FROM mcr.microsoft.com/playwright:v1.43.0-jammy

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY app ./app
COPY accounts ./accounts

ENV NODE_ENV=production

CMD ["node", "app/index.js"]
