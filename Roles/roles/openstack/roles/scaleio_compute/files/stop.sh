#!/bin/bash

systemctl stop scini

sleep 2
systemctl stop libvirtd

sleep 2
systemctl restart openstack-nova-compute

sleep 2
systemctl restart openvswitch

sleep 2
systemctl restart neutron-openvswitch-agent
