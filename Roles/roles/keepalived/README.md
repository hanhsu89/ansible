Keepalived
=========

https://www.keepalived.org/download.html


Install Keepalived
------------

1. Update group hosts in file hosts: [keepalived]
2. Update variables in vars/main.yml
	keepalived_router_id: "55"
	keepalived_check_process: "haproxy"

	keepalived_auth_pass: "1111"

	keepalived_shared_iface: "ens192"
	keepalived_shared_ip: "192.168.10.45"

3. Run:

	ansible-playbook -i hosts  site.yml --limit='keepalived' --tags=keepalived