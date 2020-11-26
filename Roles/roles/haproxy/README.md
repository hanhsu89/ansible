HAProxy
=========

// Link update version
http://www.haproxy.org/download/

https://upcloud.com/community/tutorials/haproxy-load-balancer-ubuntu/


Install HAProxy
------------

#=== From source
Compiling HAProxy for Prometheus
First, you’ll need to compile HAProxy with the Prometheus Exporter. You’ll find instructions in the README. The commands look like this on an Ubuntu server:

sudo apt update
sudo apt install -y git ca-certificates gcc libc6-dev liblua5.3-dev libpcre3-dev libssl-dev libsystemd-dev make wget zlib1g-dev
git clone https://github.com/haproxy/haproxy.git
cd haproxy
make TARGET=linux-glibc USE_LUA=1 USE_OPENSSL=1 USE_PCRE=1 USE_ZLIB=1 USE_SYSTEMD=1 EXTRA_OBJS="contrib/prometheus-exporter/service-prometheus.o"
sudo make install-bin
view raw
Note that when cloning from the git repository, you’re using the latest, cutting-edge code. If you previously installed HAProxy using your system’s package manager, execute these commands as well:

sudo systemctl stop haproxy
sudo cp /usr/local/sbin/haproxy /usr/sbin/haproxy
sudo systemctl start haproxy
view raw
Afterwards, verify that the Prometheus Exporter has been included in the compiled executable:

haproxy -vv

Built with the Prometheus exporter as a service

https://www.haproxy.com/blog/haproxy-exposes-a-prometheus-metrics-endpoint/


#=== 
http://www.haproxy.org/download/{{ haproxy_major }}/src/haproxy-{{ haproxy_version }}.tar.gz




===>
Afterwards, verify that the Prometheus Exporter has been included in the compiled executable:

haproxy -vv

Built with the Prometheus exporter as a service