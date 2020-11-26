Blackbox exporter
================


The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP and ICMP.
    - Ping
    - Monitor SSL websites


https://toivietblog.com/linux/monitoring/monitor-website-va-ssl-voi-blackbox-exporter/
Nếu bạn gặp lỗi không hiển thị một số panel trên dashboard thì gõ lệnh dưới đây để cài đặt các plugin cần thiết.

  grafana-cli plugins install grafana-image-renderer
  grafana-cli plugins install camptocamp-prometheus-alertmanager-datasource
  grafana-cli plugins install grafana-piechart-panel

Và sau đó, restart dịch vụ grafana.

  service grafana-server restart

#=== Documents

https://github.com/prometheus/blackbox_exporter
https://github.com/prometheus/blackbox_exporter/releases
https://github.com/prometheus/blackbox_exporter/blob/master/example.yml

https://www.robustperception.io/icmp-pings-with-the-blackbox-exporter

https://toivietblog.com/linux/monitoring/cai-dat-prometheus-blackbox-exporter-tren-ubuntu-18/
https://toivietblog.com/linux/monitoring/monitor-website-va-ssl-voi-blackbox-exporter/
https://toivietblog.com/linux/monitoring/monitor-ping-host-voi-blackbox-exporter/


https://devconnected.com/how-to-install-and-configure-blackbox-exporter-for-prometheus/
GrafanaID: 7587
https://grafana.com/grafana/dashboards/7587


#=== Binding the Blackbox exporter with Prometheus
Important note: in this section, Prometheus is going to scrape the Blackbox Exporter to gather metrics about the exporter itself.

To configure Prometheus to scrape HTTP targets, head over to the next sections.

To bind the Blackbox exporter with Prometheus, you need to add it as a scrape target in Prometheus configuration file.

If you follow the Prometheus setup tutorial, your configuration file is stored at /etc/prometheus/prometheus.yml

Edit this configuration file, and amend the following changes

$ sudo nano /etc/prometheus/prometheus.yml

global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
    - targets: ['localhost:9090', 'localhost:9115']

Head over to your Prometheus target configuration (http://localhost:9090/targets), and check that you are correctly scrapping your Blackbox exporter.


#=== Monitoring HTTPS endpoints with the Blackbox Exporter
In our setup, Prometheus is now currently sitting behind a reverse proxy (NGINX) configured with self signed certificates.

This is the endpoint we are going to monitor with the Blackbox Exporter.

a – Creating a Blackbox module
To monitor Prometheus, we are going to use the HTTP prober.

Head over to your Blackbox configuration file, erase its content and paste the following configuration.

modules:
  http_prometheus:
    prober: http
    timeout: 5s
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2"]
      method: GET
      fail_if_ssl: false
      fail_if_not_ssl: true
      tls_config:
        insecure_skip_verify: true
      basic_auth:
        username: "username"
        password: "password"

Here are the details of the parameters we chose.

fail_if_not_ssl: as we are actively monitoring a HTTPS endpoint, we need to make sure that we are retrieving the page with SSL encryption. Otherwise, we count it as a failure;

insecure_skip_verify: if you followed our previous tutorial, we generated our certificates with self-signed certificates. As a consequence, you are not able to verify it with a certificate authority;

basic_auth: the reverse proxy endpoint is configured with a basic username/password authentication. The Blackbox exporter needs to be aware of those to probe the Prometheus server.