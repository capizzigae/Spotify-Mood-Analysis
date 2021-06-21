#!/usr/bin/env bash
# Stop
docker stop kibana

#  Remove previuos container 
docker container rm kibana

# Build
docker build ../kibana/ --tag sp:kibana

docker stop kibana
docker run -p 5601:5601 --ip 172.18.0.52 --network spotifyMood sp:kibana
