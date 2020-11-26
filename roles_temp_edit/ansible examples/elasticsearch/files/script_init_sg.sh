 bash sgadmin.sh --enable-shard-allocation -cert /etc/elasticsearch/ssl/kirk.pem -key /etc/elasticsearch/ssl/kirk.key -cacert /etc/elasticsearch/ssl/root-ca.pem  -keypass dV59Wo0nJ2k1 -nhnv -h 127.0.0.1 -p 9300

 ./sgadmin.sh -cd ../sgconfig/ -icl -nhnv -cacert /etc/elasticsearch/ssl/root-ca.pem -cert /etc/elasticsearch/ssl/kirk.pem -key /etc/elasticsearch/ssl/kirk.key -keypass dV59Wo0nJ2k1
