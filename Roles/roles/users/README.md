#==== Guide

1. Add new user:
	+ Add hosts so that user can access to hosts_user file
	+ Add hosts so that user can access to: /vars/main.yml
		  - name: test
		    servers:
		      #[vm30]
		      192.168.206.250   # TEST
	+ Add ssh-key of new user to /public_keys/{user_name}.pub
	+ Run:
		ansible-playbook -i hosts_user playbook.yml --limit='vm30' --tags='users' -u hanhnn -K

2. Remove user:
	+ Add user need remove to /vars/main.yml
		#----REMOVE USER------------
		absent_users:
		      - anhpt
	+ Run:
		ansible-playbook -i hosts_user playbook.yml --limit='vm30' --tags='absent_users' -u hanhnn -K

3. Add user exist to new VMs:
