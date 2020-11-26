#!/bin/bash
export autoIdBegin={{autoIdBegin}}
export gsId={{gsId}}
export gameGNetPort={{gameGNetPort}}
export iwebServerPort={{iwebServerPort}}
export startServerTime="{{startServerTime}}"
export zoneName="{{zoneName}}"
export logServerIp=127.0.0.1
export uniqnameIp=192.168.31.229
export rechargeIp=192.168.31.240
export httpServerIp=192.168.31.230
export httpServerBackPort=8080
export user={{user}}
export s_new={{s_new}}
export dir_server="/home/$user/$s_new/jane.properties"

function setup_server() {
 abc=`ls /home/ |grep $user|wc -l`
 if [[ $abc == 1 ]];then
   echo "Đã tồn tại user $user"
 else
   useradd $user
   sleep 5
   cp -r /data/source/dist /home/$user/$s_new
   chown -R $user:$user /home/$user/$s_new
    echo " $s_new chạy với quyền user $user"
 fi
}

function change_idserver() {
 sed -i "s/self_id_begin/$autoIdBegin/" $dir_server
 sed -i "s/self_gs_id/$gsId/" $dir_server
 sed -i "s/self_server_name/$zoneName/" $dir_server

  id_server_auto=`grep "autoIdBegin" $dir_server |awk -F "=" '{print $2}'`
  id_server_gs=`grep "gsId" $dir_server |awk -F "=" '{print $2}'`
  name_server=`grep "zoneName" $dir_server |awk -F "=" '{print $2}'`
  echo " ID Server: $gsId"
  echo " Name_$s_new: $name_server"
}


function port_sevice() {
 sed -i "s/self_game_port/$gameGNetPort/" $dir_server
 sed -i "s/self_iweb_port/$iwebServerPort/" $dir_server
  port_game=`grep "gameGNetPort" $dir_server |awk -F "=" '{print $2}'`
  port_gmtool=`grep "iwebServerPort" $dir_server |awk -F "=" '{print $2}'`
  echo " PORT: -GAME:   $port_game
       -GMTOOL: $port_gmtool"
}

function change_default() {
  sed -i "s/self_logserver_ip/$logServerIp/" $dir_server
  sed -i "s/self_uniqname_id/$uniqnameIp/" $dir_server
  sed -i "s/httpServerIp = self_recharge_ip/httpServerIp = $httpServerIp/" $dir_server
  sed -i "s/rechargeIp = self_recharge_ip/rechargeIp = $rechargeIp/" $dir_server
  sed -i "s/self_recharge_port_callback/$httpServerBackPort/" $dir_server

  logserver=`grep "logServerIp" $dir_server |awk -F "=" '{print $2}'`
  uniqname=`grep "uniqnameIp" $dir_server |awk -F "=" '{print $2}'`
  httpserverip=`grep "httpServerIp" $dir_server |awk -F "=" '{print $2}'`
  rechargeip=`grep "rechargeIp" $dir_server |awk -F "=" '{print $2}'`
  port_callback=`grep "httpServerBackPort" $dir_server |awk -F "=" '{print $2}'`
  echo " IP Logserver: $logserver"
  echo " IP Uniqname: $uniqname"
  echo " IP Httpserver(Payment): $httpserverip"
  echo " IP Manager server (Liên server): $rechargeip"
  echo " Port callback httpserver: $port_callback"
  sleep 30
  check=`ll /home/$user/s_new/ |grep $user |wc -l`
  if [[ check == 27 ]]; then
      su - $user -c "/home/$user/$s_new/start.sh"
      echo "----------start $s_new----------"
  else
    echo "ERROR"
  fi
}

function time_server() {
  sed -i "s/self_server_start_time/$startServerTime/" $dir_server
  time_start=`grep "startServerTime" $dir_server |awk -F "=" '{print $2}'`
  echo " TIME START SERVER: $time_start "
}

function ip_server {
   ip_public=`ip a |grep "global em1" |awk  '{print $2}' |cut -d "/" -f1`
   ip_private=`ip a |grep "global em2" |awk  '{print $2}' |cut -d "/" -f1`
   echo " IP Puclic $s_new: $ip_public"
   echo " IP Private $s_new: $ip_private"
}


setup_server
time_server
change_idserver
ip_server
port_sevice
change_default
