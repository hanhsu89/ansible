#!/bin/bash

echo $(date "+%F %r") "$1 $2 has transitioned to the $3 state" > /var/run/keepalived_status