#!/usr/bin/env bash
docker container stop $(docker container ls -aq)
docker container rm $(docker container ls -aq)
docker image prune -f
docker build -t foo . && docker run -d -p 5000:5000 foo
