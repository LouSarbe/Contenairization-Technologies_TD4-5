#!/bin/bash
docker network create --driver=bridge my-tiny-network 2>/dev/null

docker run -d --name CT_PW04_Louis_BESSARD-app --network my-tiny-network -p 8080:8080 app

docker run -d --name CT_PW04_Louis_BESSARD-db --network my-tiny-network -p 5432:5432 db