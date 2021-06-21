#!/usr/bin/env bash
# Stop
docker stop pyspark

# Remove previuos container 
docker container rm pyspark

docker build ../spark/ --tag sp:spark
docker run -e SPARK_ACTION=pyspark --network=spotifyMood --name pyspark -it sp:spark