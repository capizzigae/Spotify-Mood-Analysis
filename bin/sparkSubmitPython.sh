#!/usr/bin/env bash
# Stop
docker stop sparkSubmit

# Remove previuos container 
docker container rm sparkSubmit

docker build ../spark/ --tag sp:spark
docker run -e SPARK_ACTION=spark-submit-python -p 4040:4040 --network spotifyMood --name sparkSubmit -it sp:spark $1 $2