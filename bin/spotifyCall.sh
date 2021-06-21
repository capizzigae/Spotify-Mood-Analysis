#DA MODIFICARE ED IMPOSTARE IN MODO CORRETTO

#docker build ../logstash-build --tag tap:spotifyMood
docker build --tag tap:spotifyMood ../script
docker run --network spotifyMood -it script listener.py
#dockedocker run --rm -it -v $PWD/pipeline/:/usr/share/logstash-build/pipeline/ tap:spotifyMood
