Docker
=========

Install:
- Docker latest
- Docker by version
- Docker Compose


Tags:
- Docker latest: docker
- Docker by version: docker-version
- Docker Compose: docker-compose


List versions:
	- CentOS
	https://download.docker.com/linux/centos/7/x86_64/stable/Packages/
	- Another OS:
	https://download.docker.com/


Run:
- ansible-playbook -i hosts site.yml --limit='docker' --tags='docker' -u root
- ansible-playbook -i hosts site.yml --limit='docker' --tags='docker-version' -u root
- ansible-playbook -i hosts site.yml --limit='docker' --tags='docker-compose' -u root