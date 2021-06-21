# Spotify-Mood-Analysis
Before Running:  
Add a setup directory in spark and put "spark-3.1.1-bin-hadoop2.7.".  
Download it from there: https://spark.apache.org/releases/spark-release-3-1-1.html

To run:  
Go to bin directory from the bash and execute in this order:  

./kafkaStartZK.sh  
./kafkaStartServer.sh  
./elasticsearch.sh  
./kibana.sh  
./logstashKafka.sh  
./sparkSubmitPython.sh spotifyM.py "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.elasticsearch:elasticsearch-spark-30_2.12:7.12.1"  

Then run listener.py from script directory  
