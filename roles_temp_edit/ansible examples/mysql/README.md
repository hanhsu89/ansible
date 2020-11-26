Install MariaDB
=========

* Installs MariaDB from repo

How to install MariaDB
-------------------------------------------

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-mysql' --tags=mysql_install
    ```

Creat script check MySQL status
-------------------------------------------

    ```bash
    $ yum install xinetd
    $ mv define_service /etc/xinetd.d
    $ echo "mysqlchk        9200/tcp" >> /etc/services
    $ MariaDB [(none)]> GRANT PROCESS, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'xinetd'@'127.0.0.1' IDENTIFIED BY 'password'; 
    $ vi script_check && mv script_check /usr/bin
    $ systemctl start xinetd
    ```
