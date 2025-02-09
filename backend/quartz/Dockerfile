FROM node:20-slim AS builder
WORKDIR /quartz/app
COPY package.json .
COPY package-lock.json* .
RUN npm ci

FROM node:20-slim
WORKDIR /quartz/app
COPY --from=builder /quartz/app/ /quartz/app/
COPY . .

RUN npm install

CMD ["npx", "quartz", "build", "--serve", "--port", "8081"]
