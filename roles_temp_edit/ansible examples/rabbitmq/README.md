Install RabbitMQ
=========

* Installs RabbitMQ from Reposites
* Config Vhosts for RabbitMQ

How to install RabbitMQ
-------------------------------------------

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-rabbitmq' --tags=rabbitmq_install
    ```

How to Join Cluster RabbitMQ
-------------------------------------------

* Edit master_hostname, master_ip in inventory
* Change erlang.cookies if you want ( 20 upcase random characters )

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-rabbitmq' --tags=rabbitmq_cluster
    ```

How to use rabbitmqadmin cli           
-------------------------------------------
* Requirement: Python 2.7

   ```bash
   $ python /usr/bin/rabbitmqadmin list users
   $ python /usr/bin/rabbitmqadmin list vhosts
   $ python /usr/bin/rabbitmqadmin list exchanges
   $ python rabbitmqadmin --username=guest --password=guest list nodes
   $ python /usr/bin/rabbitmqadmin --username=guest --password=guest list nodes
   $ python /usr/bin/rabbitmqadmin --username=guest --password=guest list queues
   $ python /usr/bin/rabbitmqadmin list exchanges
   ```
