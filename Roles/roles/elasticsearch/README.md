ElasticSearch
=========

#===> heap-size-settings
https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html#heap-size-settings


===> Important System Configuration
https://www.elastic.
co/guide/en/elasticsearch/reference/current/system-config.html

Configuring system settings
Disable swapping
File Descriptors
Virtual memory
Number of threads
DNS cache settings
JNA temporary directory not mounted with noexec
TCP retransmission timeout

Disable swapping
Increase file descriptors
Ensure sufficient virtual memory
Ensure sufficient threads
JVM DNS cache settings
Temporary directory not mounted with noexec
TCP retransmission timeout


Virtual memory
https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
sysctl -w vm.max_map_count=262144










===> Backup & Restore cluster:
https://www.elastic.co/guide/en/elasticsearch/reference/current/backup-cluster.html