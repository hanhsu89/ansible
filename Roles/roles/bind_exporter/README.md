bind_exporter_Monitor Bind9 DNS
==================================


Dashboard
    https://grafana.com/grafana/dashboards/12309



===> Prometheus Configuration
- job_name: 'bind_exporter'
  scrape_interval: 15s
  metrics_path: '/metrics'
  static_configs:
  - targets:
    - ip-server-dns01:9119
    - ip-server-dns02:9119