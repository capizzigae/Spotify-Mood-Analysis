#!/usr/bin/env bash
#REM Stop
docker stop sp:spotifyMood

#REM Remove previuos container 
docker container rm sp:spotifyMood

#REM Build
docker build ../logstash-build --tag sp:spotifyMood

docker stop sp:spotifyMood
#REM Run
docker run --rm -it -v $PWD/../logstash-build/pipeline/:/usr/share/logstash/pipeline/ -p 8192:8192 --network=spotifyMood sp:spotifyMood