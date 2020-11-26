GlusterFS - Heketi
=========


Install:
1. GluterFS:
		- Standalone
		- Cluster
2. Heketi		
-------------------------------

#======== Guide
	1. Edit hosts file:
	[glusterfs]
	192.168.10.42 	host_gfs=192.168.10.42 name_gfs=gfs-1
	192.168.10.43	host_gfs=192.168.10.43 name_gfs=gfs-2
	192.168.10.44	host_gfs=192.168.10.44 name_gfs=gfs-3
	[heketi]
	192.168.10.42	host_heketi=192.168.10.42 name_heketi=heketi
	
	2. Edit var/main.yml

	3. If host number > 3 => Update host in task name: Update host to /etc/hosts (./task/glusterfs.yml)

	4. Run:
		+ GlusterFS_Install:
		ansible-playbook -i hosts site.yml --limit='glusterfs' --tags='glusterfs' -u root

		+ Heketi_Install
		 ansible-playbook -i hosts site.yml --limit='heketi' --tags='heketi' -u root

#========
	Dependencies between Volume types and sizes:

	Available GlusterFS Volume types		Volume space calculations

	Distributed (for maximum space)			1G + 1G = 2G
	Replicated (for high availability)		1G + 1G = 1G
	Striped (for large files)				1G + 1G = 2G
	Distributed and Replicated				(1G+1G) + (1G+1G) = 2G
	Distributed and Stripped 				(1G+1G) + (1G+1G) = 4G
	Distributed, Replicated and Stripped	[(1G+1G)+(1G+1G)] + [(1G+1G)+(1G+1G)] = 4G

#======= Increasing Cluster Size
1. Using Heketi CLI: 
	heketi-cli node add --zone=1 --cluster=8f2157cbed10651e18199a07814228a8 --management-host-name=gfs-4 --storage-host-name=192.168.10.31

	==> Output:
	Node information:
	Id: 8f9471e88d8efc597cd70d73601125c4
	State: online
	Cluster Id: 8f2157cbed10651e18199a07814228a8
	Zone: 1
	Management Hostname gfs-4
	Storage Hostname 192.168.10.31

	#===
	To register /dev/sdb and /dev/sdc devices for 095d5f26b56dc6c64564a9bc17338cbf node:
	heketi-cli device add --name=/dev/sdb --node=095d5f26b56dc6c64564a9bc17338cbf
	==> Output:
	Device added successfully

2. Updating Topology File
	- Add a new node and devices
	- Load the topology file

#======> Documents:

https://docs.openshift.com/container-platform/3.5/install_config/storage_examples/dedicated_gluster_dynamic_example.html

1. https://www.mankier.com/8/heketi-cli
2. https://wiki.centos.org/HowTos/GlusterFSonCentOS
3. https://access.redhat.com/documentation/en-us/red_hat_gluster_storage/3.3/html/container-native_storage_for_openshift_container_platform/chap-documentation-red_hat_gluster_storage_container_native_with_openshift_platform-managing_clusters