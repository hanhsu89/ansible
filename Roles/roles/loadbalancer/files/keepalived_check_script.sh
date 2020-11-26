#!/bin/bash

killall -0 haproxy >/dev/null

if [[ "$?" -eq 1 ]]
then
  echo 'Haproxy is down!' | logger -p alert -t keepalived_check_script.sh
  exit 1
fi

exit "$?"