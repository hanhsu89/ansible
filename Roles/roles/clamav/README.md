ClamAV antivirus
=========
clamav-ansible-role
Ansible role to install and configure ClamAV antivirus on CentOS/RHEL. SELinux enabled servers are supported.

=========
Requirements
CentOS/RHEL 7
Installation
$ ansible-galaxy install zaxos.clamav-ansible-role
Example Playbook
- hosts: servers

  roles:
    - role: zaxos.clamav-ansible-role

=========
Role Variables
Some variables that require review:

clamav_freshclam_autoupdate_service: True
If set to "True", a freshclam service for automatic antivirus definitions updates will be created.
clamav_freshclam_daily_checks_for_updates: 2
Number of freshclam service definitions update checks per day. Default is set to 2 checks per day.
clamav_freshclam_geolocation_based_update_server: True
If set to "True", this playbook will try to pinpoint your country using geolocation service "ipinfo.io" in order to find the best possible freshclam update server. Set to "False" to remove any geolocation based update server.
clamav_freshclam_update_on_every_run: False
If set to "True", this playbook will perform antivirus definitions update using freshclam on every playbook run. By default, definitions update will be performed on ClamAV installation (first playbook run).