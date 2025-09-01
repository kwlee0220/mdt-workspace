#! /bin/bash

docker image rmi $1/mdt-client

cp ../mdt-client-all.jar mdt-client-all.jar

docker build -t $1/mdt-client:latest .
docker push $1/mdt-client:latest

rm mdt-client-all.jar
