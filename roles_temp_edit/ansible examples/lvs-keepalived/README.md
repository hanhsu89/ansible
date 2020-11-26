Role for install and configure LVS|Keepalived cluster
=====================================================

0. **Documentation**

- Research on LVS/Keepalived conjunction and manual instructions:
<https://docs.google.com/spreadsheets/d/1asoIjATWdit-7FFsxdrmGPfvxA_y3Dg-6C8LaPDv0Wo/edit?usp=sharing>

1. **Requirement**

- OS: CentOS 7
- Services are listening on specified real servers.

2. **Update inventory and variables**

    hosts
    ```
    [director]
    192.168.10.150 viface="ens160"   ### keepalived will assign virtual IP to the interface specified with "viface"
    192.168.10.149 viface="ens160"

    [realserver]
    192.168.10.151
    192.168.10.152
    ```

    vars (defaults/main.yml)
    ```yaml
    keepalived_auth_pass: "1111"
    keepalived_router_id: "52"
    keepalived_virtual_ip: "192.168.10.153"
    keepalived_virtual_mask: "24"
    keepalived_priority: "200"
    keepalived_backup_priority: "100"
    lvs_virtualservers:
      - healthcheck_interval: "6"
        virtual_port: "80"
        lvs_method: "DR"
        lvs_sched: "rr"
        protocol: "tcp"
        realservers:
          - ip: "192.168.10.151"
            port: "80"
            weight: "1"
            healthcheck_timeout: "3"
            healthcheck_retry: "3"
          - ip: "192.168.10.152"
            port: "80"
            weight: "1"
            healthcheck_timeout: "3"
            healthcheck_retry: "3"
    ```

3. **Command to setup all nodes - for testing**

    ```bash
    cd examples/
    ansible-playbook playbook.yml -i hosts
    ```

4. **TODO**

- Testing.
- Optimizing.
