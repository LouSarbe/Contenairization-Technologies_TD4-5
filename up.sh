#!/bin/bash
docker volume create db-vol

docker run -d --name CT_PW04_Louis_BESSARD-db \
  --network my-tiny-network \
  -e POSTGRES_USER=LouSarbe \
  -e POSTGRES_PASSWORD=Password01 \
  -e POSTGRES_DB=CT_PW04-database \
  -v db-vol:/data \
  db

docker run -d --name CT_PW04_Louis_BESSARD-app \
  --network my-tiny-network \
  -p 8080:8080 \
  app