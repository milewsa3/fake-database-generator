#!/usr/bin/bash -ue

docker build --progress=plain --build-arg OPENAI_API_KEY=$OPENAI_API_KEY --build-arg NUMBER_OF_TABLES=7 -t milewsa3/fdg .
docker stop $(docker ps -aq)
docker run -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword milewsa3/fdg