1. Deploy GW Internet for CentOS 7:

- Edit roles for server in file after_hosts
- Edit variables in file /vars/main.yml
- How to run:
    
    ```bash
    $ansible-playbook -i after_hosts site.yml --limit='web-server' -u hoanpv --tags=gw_internet
    ```
