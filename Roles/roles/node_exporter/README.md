Node Exporter
==================================


Dashboard
    https://grafana.com/grafana/dashboards/1860
    https://grafana.com/grafana/dashboards/11074



===> Prometheus Configuration
Add to Prometheus config
  - job_name: node-exporter
    static_configs:
    - targets:
      - 192.168.1.30:9100
        labels:
          host: 'vm30'