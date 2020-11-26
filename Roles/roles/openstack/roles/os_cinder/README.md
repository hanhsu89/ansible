Role's roles
------------

Setting up and configuring cinder (Openstack Block Storage) to provide block device to instances.

This role is going to do the following:
* Create database for cinder and ensure priviledges to `cinder` user
* Create configured service/user/endpoint and the mapping user(s) <=> role(s)
* Supported backends: scaleio, lvm.
* Config /var/main.yml if you want fix my config.

Requirements
------------

* A running database (MySQL/MariaDB) SQL server
* A running keystone (identity service) for user/role mapping/service/endpoint creating.

