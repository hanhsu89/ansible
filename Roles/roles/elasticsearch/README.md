ElasticSearch
=========


https://github.com/elastic/ansible-elasticsearch/releases


// Check version
    curl http://localhost:9200/_cluster/health?pretty -u elastic:dF4pwhoz0b65RxF23hLA
    curl -XGET 'http://localhost:9200' -u elastic:dF4pwhoz0b65RxF23hLA
    
    usr/share/elasticsearch/bin# ./elasticsearch --version
    Version: 7.10.1, Build: default/deb/1c34507e66d7db1211f66f3513706fdf548736aa/2020-12-05T01:00:33.671820Z, JVM: 15.0.1


Type	Description	Default Location	            Setting
home	Elasticsearch home directory or $ES_HOME	/usr/share/elasticsearch	
bin	    Binary scripts including elasticsearch to start a node and elasticsearch-plugin to install plugins	/usr/share/elasticsearch/bin	
conf	Configuration files including elasticsearch.yml	    /etc/elasticsearch	ES_PATH_CONF
conf	Environment variables including heap size, file descriptors.	/etc/default/elasticsearch	
data	The location of the data files of each index / shard allocated on the node. Can hold multiple locations.	/var/lib/elasticsearch	path.data
jdk	    The bundled Java Development Kit used to run Elasticsearch. Can be overridden by setting the JAVA_HOME environment variable in /etc/default/elasticsearch.	/usr/share/elasticsearch/jdk	
logs	Log files location.	/var/log/elasticsearch	path.logs
plugins	Plugin files location. Each plugin will be contained in a subdirectory.	/usr/share/elasticsearch/plugins	
repo	Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here.	Not configured	path.repo


// Sau khi install done => into /usr/share/elasticsearch/bin chay lenh: 
    ./elasticsearch-setup-passwords auto
    => get password access elastic

    config /etc/kibana/kibana.ym => add password da gen o tren vao file config
        Changed password for user elastic
        PASSWORD elastic = dF4pwhoz0b65RxF23hLA


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