FROM docker.elastic.co/logstash/logstash:7.11.2

# Add your logstash plugins setup here

#RUN bin/logstash-plugin install logstash-tcp-input

# to build with
# docker build . --tag sp:spotifyMood
# and run with (from logstash-build directory)


#docker run --rm -it -v $PWD/pipeline/:/usr/share/logstash/pipeline/ -p 8192:8192 pr:spotifyMood
#to run from directory
#docker run --rm -it -v $PWD/pipeline/:/usr/share/logstash/pipeline/ -p 8192:8192 --network=spotifyMood sp:spotifyMood

# make sure that pipeline dir with proper conf is there
# NOTE: need to add the publish port ( -p 8192:8192) and the network (spotifyMood) at the run