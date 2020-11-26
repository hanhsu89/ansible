#!/bin/sh

# Reset iptables
iptables -F INPUT
iptables -F FORWARD
iptables -F OUTPUT
# Ghi chú:
#   không dùng iptables -F/-X vì làm lỗi docker (xóa nhầm cả Chain DOCKER)
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Allow anything on loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
# Allow ICMP
# http://serverfault.com/a/84981
iptables -A INPUT -p icmp -j ACCEPT

# Allow ssh connections to server

iptables -A INPUT -s 0.0.0.0 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -s 0.0.0.0 -p tcp --dport 1102 -j ACCEPT
iptables -A INPUT -s 0.0.0.0 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT


# Save settings
/etc/init.d/iptables save
