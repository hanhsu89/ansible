#!/bin/bash


if [ ! -f after_hosts ]; then

  echo "Please generate file after_hosts from file example_inventory before run this scripts"

else

  ssh-keygen -t rsa -f /tmp/id_rsa -N '' -C root@ci-cd
  ansible-playbook -i after_hosts playbook.yml
  rm -rf /tmp/id_rsa*
  
fi