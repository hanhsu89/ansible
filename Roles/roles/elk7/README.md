Role Name
=========

Install Elasticsearch Cluster

Descriptions
------------

* Elastic Cluster with 3 roles:
   - Master
   - Data
   - Client

* Install Kibana in Node Client

Role Variables
--------------

* version
* cluster_name
* master_nodes
* minimum_master_nodes
* data_dir
* log_dir
* config_dir
* home_dir

How to run
----------

* Install Cluster

	```bash
	$ ansible-playbook -i after_hosts playbook.yml --limit='example-elasticsearch' --tags=elasticsearch_install
	```

* Uninstall Complete

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-elasticsearch' --tags=elasticsearch_uninstall
    ```

Support Version
---------------

* Ansible 2.6
* CentOS 7

Notes
-----

* Relocate shard unassign

        POST _cluster/reroute
        {
            "commands": [{
                "allocate_stale_primary": {
                    "index": ".monitoring-kibana-6-2018.09.08",
                    "shard": 0,
                    "node": "demo52",
                    "accept_data_loss": true
                }
            }]
        }

* Common cluster command

    ```bash
    $ curl -XGET http://localhost:9200/_cat/shards
    $ curl -XGET localhost:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason| grep UNASSIGNED
    $ curl -XGET localhost:9200/_cluster/allocation/explain?pretty
    $ curl -XGET 'localhost:9200/.monitoring-kibana-6-2018.09.08/_settings'
    $ curl localhost:9200/_cat/health?v
    $ curl localhost:9200/_cat/nodes?v
    
    ```

* Set default Shards and Replicas

    ```bash
    PUT _template/default
    {
      "index_patterns": ["*"],
      "settings": {
      "number_of_shards": "3",
      "number_of_replicas": "1"
    }
    }
    ```
