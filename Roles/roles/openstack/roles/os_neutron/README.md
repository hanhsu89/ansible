Role's roles
------------

Setting up and configuring `neutron` (Openstack Network Service) which provide ingress/egress network connectivity to/from instances.

This role is going to do the following:

* Create SQL Database and ensure priviledges to `neutron` user
* Create configured Neutron service/endpoint/user and the mapping user(s) <=> role(s)
* Supported network scenario: provider & self-service network (config neutron_network_options in vars/main.yml)
* Supported provider network types: flat, vlan
* Supported tenant network types: vlan, vxlan, gre
* Supported neutron plugins: openvswitch

Requirements
------------

* A running database (MySQL/MariaDB)
* A running keystone (identity service) for user/role mapping/service/endpoint creating.

How to use
-----------

* Setup controller with task:
    + neutron_install.yml
    + neutron_service_setup.yml
    + neutron_db_setup.yml

* Setup network node with task:
    + neutron_node_install

* Change config using tags:
    + neutron_controller_config for change config controller
    + neutron_node_config for change config network node