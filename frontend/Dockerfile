# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY ./fronted/package*.json ./
RUN npm install
COPY ./fronted/ ./
RUN npm run build
CMD cp -r build result_build
