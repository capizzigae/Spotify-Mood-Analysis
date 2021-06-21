#!/usr/bin/env bash
# Stop
docker stop kafkaZK

# Remove previuos container 
docker container rm kafkaZK

docker build ../kafka --tag sp:kafka
docker run -e KAFKA_ACTION=start-zk --network=spotifyMood --ip 172.18.0.22 -p 2181:2181 --name kafkaZK -it sp:kafka
