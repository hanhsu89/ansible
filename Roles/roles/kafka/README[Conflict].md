Kafka
==================================

https://vsudo.net/blog/gia-tri-mac-dinh-kafka.html

Default Ports
Port    Description
2181    Client connection port
2888    Quorum port for clustering
3888    Leader election port for clustering

What is the maximum replication factor for a partition of kafka topic
Replication factor determines the number of replications each partition have, this allows Kafka to automatically failover to these replicas when a server in the cluster fails so that messages remain available in case of failures

Partition replicas are distributed across brokers and one broker should keep one replica that means we can't have more replicas than the number of brokers

Max Replication factor <= brokers number.

This is also meant to determine min.insync.replicas, that means it will always be less than or equal to replication-factor

min.insync.replicas means <= Replication factor

min.insync.replicas is the minimum number of copies of the data that you are willing to be online at any time to continue running and accepting new incoming messages.

Ideally replication factor 3 is good as mentioned above, however, based on the use case you can tune replication factor less than 2 (means high risk) and the same time more than 3 provide better availability but more overhead and more size required.



===> Command
  https://docs.cloudera.com/documentation/kafka/latest/topics/kafka_command_line.html

=> Show topic
  /usr/share/kafka/bin#
  ./kafka-topics.sh --zookeeper localhost:2181 --list
  OR
  ./zookeeper-shell.sh localhost:2181 ls /brokers/topics
  ./zookeeper-shell.sh kafka1.service.staging.fwork,kafka2.service.staging.fwork,kafka3.service.staging.fwork ls /brokers/topics

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

  --replication-factor  => Số bản sao topic

=> Delete topic ( Add line delete.topic.enable=true to server.properties)
  ./kafka-topics.sh --zookeeper localhost:2181 --delete --topic test

=> Add events/messages into the topic
  ./kafka-console-producer.sh --topic hanhsu --bootstrap-server localhost:9092

=> Show events/message in topic
  ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic send-email --from-beginning

  
=> Show detail of Topics
  ./kafka-topics.sh --describe --zookeeper localhost:2181
  ./kafka-topics.sh --describe --zookeeper localhost:2181 --topic topic_name
  ./kafka-topics.sh --describe --zookeeper kafka1.service.staging.fwork,kafka2.service.staging.fwork,kafka3.service.staging.fwork --topic send-email --max-messages 1

Topic: send-email       PartitionCount: 3       ReplicationFactor: 1    Configs: 
        Topic: send-email       Partition: 0    Leader: 2       Replicas: 2     Isr: 2
        Topic: send-email       Partition: 1    Leader: 0       Replicas: 0     Isr: 0
        Topic: send-email       Partition: 2    Leader: 1       Replicas: 1     Isr: 1

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


#======== Note =======
#/opt/zookeeper-3.4.9/conf/zoo.cfg

#server.1=master:2888:3888
#server.2=slave1:2888:3888
#server.3=slave2:2888:3888