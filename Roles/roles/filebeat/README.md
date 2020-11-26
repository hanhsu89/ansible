Install Filebeat
================

* Installs Filebeat

How to install Filebeat
-----------------------

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-filebeat' --tags=filebeat_install
    ```

How to uninstall Filebeat
-----------------------                    

    ```bash
    $ ansible-playbook -i after_hosts playbook.yml --limit='example-filebeat' --tags=filebeat_uninstall
    ```
