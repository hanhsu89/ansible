#!/bin/bash

user="{{user}}"
server_game="{{server_game}}"
dir_source=/data/source/dist

function close_iptables() {
   iptables-restore < /usr/local/bin/close_iptables
}

function open_iptables() {
   iptables-restore < /usr/local/bin/open_iptables
}

function work() {
set -f
while [ -n "$user" ]
do
    set -- $user; i=$1; shift; user=$*
    set -- $server_game; j=$1; shift; server_game=$*
    echo "$i $j"
         su - $i -c "/home/$i/$j/stop.sh"
         sleep 30
         rm -rf /home/$i/$j/arpg_server.jar
         echo "REMOVE arpg_server.jar"
         rm -rf /home/$i/$j/lib
         echo "REMOVE lib"
         cp $dir_source/arpg_server.jar /home/$i/$j/
         echo "UPDATE arpg_server.jar done"
         cp $dir_source/lib /home/$i/$j/ -r
         echo "UPDATE lib done"
         chown -R $i:$i /home/$i/$j/
         echo "CHOWN /home/$i/$j"
         su - $i -c "/home/$i/$j/start.sh"
         echo "------------------start $j"
      done
}

close_iptables
sleep 60
work
open_iptables
