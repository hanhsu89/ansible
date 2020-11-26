K8s_vm
=========


Steps prepare for VM to build K8s cluster
------------

Include:

1. Check & disable firewalld
2. Check & enable ntpd/ntpdate
3. Change hostname OS
4. Update OS
5. Setup network (GW Internet, DNS): BlogSG, AppvnSG	=> Option
6. Install docker by version (v19.03.5)

------------
Steps:
1. Change vars/main.yml
	+ hostname: k8s-node
	+ docker_version: "19.03.5"

2. Change IP server in hosts
	[k8s_vm]
	192.168.10.44

3. Run
	ansible-playbook -i hosts site.yml --limit='k8s_vm' --tags=k8s_vm -u root