Install Redis
=========

* Installs Redis from Source

How to install Redis Standalone
-------------------------------

1. **Change roles/redis/vars/main.yml**
  - redis_version
  - redis_port

2. **Command to run setup**

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-redis' --tags=redis_install
    ```
How to install Redis Sentinel
-----------------------------

1. **Change roles/redis/vars/main.yml**
  - redis_version
  - redis_port
  - sentinel_port (redis-port + 20000)
  - sentinel_master_node ( the same as ip of host in inventory )
  - sentinel_quorum ( total_host/2 + 1)

2. **Command to run setup**

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-redis' --tags=redis_sentinel
    ```

How to Complete Uninstall
-------------------------

1. **Command to run uninstall**

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-redis' --tags=redis_uninstall
    ```