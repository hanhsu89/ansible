Install Node Exporter as a Servivce
==================================

* Installs Node Exporter to monitor with prometheus

How to install 
--------------

1. **Command to run setup**

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-redis' --tags=node_exporter
    ```
