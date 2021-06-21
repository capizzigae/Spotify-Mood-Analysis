#!/usr/bin/env bash
# Stop
docker stop elasticsearch

# Remove previuos container 
docker container rm elasticsearch

# Build
docker build ../elasticsearch/ --tag sp:elasticsearch

docker run -t  -p 9200:9200 -p 9300:9300 --ip 172.18.0.51 --name elasticsearch --network spotifyMood -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms4g -Xmx4g" sp:elasticsearch
