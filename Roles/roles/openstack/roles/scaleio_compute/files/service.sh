#!/bin/bash

systemctl restart scini

systemctl restart libvirtd

systemctl restart openstack-nova-compute

systemctl restart openvswitch

systemctl restart neutron-openvswitch-agent
