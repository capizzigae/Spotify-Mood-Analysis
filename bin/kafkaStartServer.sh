#!/usr/bin/env bash
# Stop
docker stop kafkaServer

# Remove previuos container 
docker container rm kafkaServer

docker build ../kafka --tag sp:kafka
docker stop kafkaServer
docker run -e KAFKA_ACTION=start-kafka --network=spotifyMood --ip 172.18.0.23 -p 9092:9092 --name kafkaServer -it sp:kafka