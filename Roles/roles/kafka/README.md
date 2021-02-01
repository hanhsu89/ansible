Kafka
==================================

Default Ports
Port    Description
2181    Client connection port
2888    Quorum port for clustering
3888    Leader election port for clustering


https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/


https://hackernoon.com/best-practices-for-apache-kafka-configuration-maf31rn
https://docs.cloudera.com/documentation/kafka/latest/topics/kafka_performance.html
https://docs.microsoft.com/en-us/azure/event-hubs/apache-kafka-configurations
https://medium.com/streamthoughts/apache-kafka-rebalance-protocol-or-the-magic-behind-your-streams-applications-e94baf68e4f2
https://medium.com/bakdata/solving-my-weird-kafka-rebalancing-problems-c05e99535435
https://stackoverflow.com/questions/47734281/kafka-consumers-rebalance-unexpectedly

https://www.cloudkarafka.com/blog/2016-11-30-part1-kafka-for-beginners-what-is-apache-kafka.html#:~:text=Broker%3A%20Handles%20all%20requests%20from,Sends%20records%20to%20a%20broker.

===> Import/Export
https://www.scaleway.com/en/docs/configure-apache-kafka/


===> Command
  https://docs.cloudera.com/documentation/kafka/latest/topics/kafka_command_line.html

https://www.baeldung.com/ops/listing-kafka-consumers

===> Show Group
./kafka-consumer-groups.sh  --list --bootstrap-server localhost:9092
group-mailer-service
notify-app
KMOffsetCache-68ee1af4194f
group-web-push
group-in-app-notification
jaeger-ingester

./kafka-consumer-groups.sh --describe --group group-mailer-service --bootstrap-server localhost:9092 

GROUP                TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                         HOST            CLIENT-ID
group-mailer-service send-email      0          10845           10845           0               mailer-backend-1e5b6740-3416-4576-a7cf-38c6b1abfc3a /10.10.35.21    mailer-backend
group-mailer-service send-email      2          4480            4480            0               mailer-backend-c8cf2467-75a3-40c8-bc5c-f6980e8f7b6c /10.10.35.18    mailer-backend
group-mailer-service send-email      1          4613            4613            0               mailer-backend-fe5075be-02ee-4303-882d-92e76c1df39f /10.10.35.17    mailer-backend


=> Show topic
  /usr/share/kafka/bin#
  ./kafka-topics.sh --zookeeper localhost:2181 --list

=> Show events/message in topic
  ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic send-email --from-beginning

=> Show detail of Topics
  ./kafka-topics.sh --describe --zookeeper localhost:2181
  ./kafka-topics.sh --describe --zookeeper localhost:2181 --topic topic_name

Topic: send-email       PartitionCount: 3       ReplicationFactor: 1    Configs: 
        Topic: send-email       Partition: 0    Leader: 2       Replicas: 2     Isr: 2
        Topic: send-email       Partition: 1    Leader: 0       Replicas: 0     Isr: 0
        Topic: send-email       Partition: 2    Leader: 1       Replicas: 1     Isr: 1


  ./zookeeper-shell.sh localhost:2181 ls /brokers/ids # Gives the list of active brokers
  ./zookeeper-shell.sh localhost:2181 ls /brokers/topics #Gives the list of topics
  ./zookeeper-shell.sh localhost:2181 get /brokers/ids/0 #Gives more detailed information of the broker id '0'
  ./zookeeper-shell.sh localhost:2181 get /brokers/ids/1
Connecting to localhost:2181
WATCHER::
WatchedEvent state:SyncConnected type:None path:null
{"listener_security_protocol_map":{"INSIDE":"PLAINTEXT","OUTSIDE":"PLAINTEXT"},"endpoints":["INSIDE://fwork-kafka2:9094","OUTSIDE://kafka2.service.staging.fwork:9092"],"jmx_port":-1,"host":"fwork-kafka2","timestamp":"1591098357682","port":9094,"version":4}


=> Create topic
  ./kafka-topics.sh --create --zookeeper localhost:2181 --topic hanhsu --partitions 3 --replication-factor 1

=> Delete topic ( Add line delete.topic.enable=true to server.properties)
  ./kafka-topics.sh --zookeeper localhost:2181 --delete --topic test

=> Add events/messages into the topic
  ./kafka-console-producer.sh --topic hanhsu --bootstrap-server localhost:9092

=> Status Cluster
  ./zookeeper-shell.sh localhost:2181 ls /brokers/ids
  ./zookeeper-shell.sh localhost:2181 ls /brokers/ids/0  # Gives more detailed information of the broker id '0'

From here you can explore the broker details using various commands:
$  ls /brokers/ids # Gives the list of active brokers
$  ls /brokers/topics #Gives the list of topics
$  get /brokers/ids/0 #Gives more detailed information of the broker id '0'


===> Tool GUI
  https://github.com/cloudhut/kowl





#======== Kafka Multi Node Cluster
  + https://github.com/lloydmeta/ansible-kafka-cluster
  + https://github.com/sanjeevmaheve/ansible-kafka-cluster.git



http://cloudurable.com/blog/kafka-tutorial-kafka-from-command-line/index.html



https://medium.com/hacking-talent/kafka-all-you-need-to-know-8c7251b49ad0


#======== Note for ZooKeeper
Each one of the components that is a part of the Zookeeper architecture has been explained below.

For standalone mode, only the below three fields are needed and meaningful:

tickTime
dataDir
clientPort


Client - Clients, one of the nodes in our distributed application cluster, access information from the server. For a particular time interval, every client sends a message to the server to let the sever know that the client is alive.Similarly, the server sends an acknowledgment when a client connects. If there is no response from the connected server, the client automatically redirects the message to another server.
Server - Server, one of the nodes in our Zookeeper ensemble, provides all the services to clients. Gives acknowledgment to client to inform that the server is alive.
Leader - Server node which performs automatic recovery if any of the connected node failed. Leaders are elected on service startup.
Follower - Server node which follows leader instruction.

#===== Check ZooKeeper
cd /usr/share/zookeeper/bin/
./zkCli.sh -server 127.0.0.1:2181
  => [zk: 127.0.0.1:2181(CONNECTED) 0]


#===== Docs
1. Install StandAlone
  + https://github.com/dixudx/ansible-zookeeper
  + https://www.howtoforge.com/how-to-setup-apache-zookeeper-cluster-on-ubuntu-1804/  
  + https://github.com/idealista/zookeeper_role


  + https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-an-apache-zookeeper-cluster-on-ubuntu-18-04
  + https://www.howtoforge.com/how-to-setup-apache-zookeeper-cluster-on-ubuntu-1804/  


  http://dixu.me/2015/10/17/Tutorial-on-ZooKeeper-Part-3-Setup-ZooKeeper-Cluster/

  https://github.com/sleighzy/ansible-kafka


#=== zookeeper cluster
https://linuxconfig.org/how-to-install-and-configure-zookeeper-in-ubuntu-18-04#h6-configure-and-setup-the-zookeeper  
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-an-apache-zookeeper-cluster-on-ubuntu-18-04

// file myid (OK)
https://github.com/dixudx/ansible-zookeeper/blob/master/templates/myid.j2

// zoo.cfg file
https://github.com/dixudx/ansible-zookeeper/blob/master/templates/zoo.cfg.j2



// Config
https://jaceklaskowski.gitbooks.io/apache-kafka/content/kafka-properties.html
https://docs.confluent.io/platform/current/kafka/deployment.html

These conditions needed to be keep in mind to change session.timeout.ms:

group.max.session.timeout.ms in the server.properties > session.timeout.ms in the consumer.properties.
group.min.session.timeout.ms in the server.properties < session.timeout.ms in the consumer.properties.
request.timeout.ms > session.timeout.ms + fetch.wait.max.ms
(session.timeout.ms)/3 > heartbeat.interval.ms
session.timeout.ms > Worst case processing time of Consumer Records per consumer poll(ms).


Another reason of this problem is not sending heartbeat in session.timeout.ms. So maybe you can consider to increase this.

heartbeat.interval.ms: The expected time between heartbeats to the consumer coordinator when using Kafka's group management facilities. Heartbeats are used to ensure that the consumer's session stays active and to facilitate rebalancing when new consumers join or leave the group. The value must be set lower than session.timeout.ms, but typically should be set no higher than 1/3 of that value. It can be adjusted even lower to control the expected time for normal rebalances.

session.timeout.ms: The timeout used to detect client failures when using Kafka's group management facility. The client sends periodic heartbeats to indicate its liveness to the broker. If no heartbeats are received by the broker before the expiration of this session timeout, then the broker will remove this client from the group and initiate a rebalance.