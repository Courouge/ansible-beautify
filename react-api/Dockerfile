# base image
FROM node:12.2.0-alpine

#ENV https_proxy http://192.168.2.1:3128
#ENV http_proxy http://192.168.2.1:3128

COPY . /app

WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json

RUN npm install --silent && npm audit fix

# start app
CMD ["npm", "start"]
