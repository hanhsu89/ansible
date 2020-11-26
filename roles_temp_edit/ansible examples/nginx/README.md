Build NGINX + PHP-FPM
=========

* Installs nginx from source based on version.
* Installs PHP-FPM from Remi repo.
* Config Vhosts for Nginx
   - Creat vhost in backend and LB
   - Config certificate support Let's Encrypt and all other vendor
   - Config get Real-IP if enable CloudFlare proxy for domain

How to install PHP-FPM for backend
-------------------------------------------
* Install PHP-FPM 5.6

    ```bash
    $ ansible-playbook -i after_hosts nginx.yml --limit='example-nginx' --tags=php5.6_install
    ```

* Install PHP-FPM 7.1

    ```bash
    $ ansible-playbook -i after_hosts nginx.yml --limit='example-nginx' --tags=php7.1_install
    ```

How to install nginx
-----------------------------
* "nginx_version" Version you want to install
* "nginx_custom_modules" Modules you want to compline with nginx
* "nginx_install_dir" Install location of nginx
* "nginx_src_dir" Directory to use for building nginx
* "nginx_group" Usergroup run nginx
* "nginx_user" User run nginx

    ```bash
    $ ansible-playbook -i after_hosts nginx.yml  --limit='example-nginx' --tags=nginx_install
    ```

How to configure vhosts
--------------------------------
* "nginx_vhost_domain" List vhost of nginx server
* "name" DomainName config for vhosts
* "upstream" Name of upstream config in loadbalancer
* "path" Path to source code in backend
* "ssl" 
   - http: only http , no ssll
   - https: ssl with non-letsencrypt certificate
   - cloudflare: use https base on proxy CloudFlare
   - letsencrypt: ssl with Let's Encrypt certificate
* "cert_name" ( only set for ssl=https ) filename's certificate use for domain
* "cert_key" ( only set for ssl=https ) filename's key use for domain
* "lb_master" ( only set for ssl=letsencrypt ) IP of server LB master where have VIP Public to generate SSL Let's Encrypt Certificate
* "backend" IP of backend server run this vhost

    ```bash
    $ ansible-playbook -i after_hosts nginx.yml  --limit='example-nginx' --tags=nginx_vhost
    ```

License
-------

OS support:
* CentOS 6
* CentOS 7
* Ubuntu 14
* Ubuntu 16
