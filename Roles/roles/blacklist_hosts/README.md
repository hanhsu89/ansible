Ansible Role: Blacklist Hosts
==================

[![Build Status](https://travis-ci.org/Lusitaniae/ansible-role-blacklist-hosts.svg?branch=master)](https://travis-ci.org/Lusitaniae/ansible-role-blacklist-hosts)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Lusitaniae/ansible-role-blacklist-hosts/master/LICENSE)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-Lusitaniae.ansible--role--blacklist--hosts-blue.svg)](https://galaxy.ansible.com/Lusitaniae/ansible-role-blacklist-hosts)


Role for installing StevenBlack hosts blacklist collection [StevenBlack](https://github.com/StevenBlack/hosts).

https://github.com/StevenBlack/hosts

Requirements
------------

* Ansible >= 2.0
* Ubuntu

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):

    hosts_blacklist_name: gambling-porn-social

    hosts_custom:
      address: 127.0.0.1
      hostnames:
        - demo.local
        - proxy.local

    hosts_whitelist:
        - www.twitter.com
        - twitter.com



Example Playbooks
-----------------

Minimal playbook:

```yaml
- hosts: localhost
  roles:
    - role: Lusitaniae.ansible-role-blacklist-hosts
```

Playbook with example configuration:

```yaml
- hosts: localhost

  vars:
    hosts_blacklist_name: gambling-porn-social
    hosts_custom:
        address: 127.0.0.1
        hostnames:
          - demo.local
          - proxy.local
    hosts_whitelist:
          - www.twitter.com
          - twitter.com

  roles:
    - role: Lusitaniae.ansible-role-blacklist-hosts

```


License
-------

MIT
