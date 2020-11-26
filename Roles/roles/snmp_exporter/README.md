SNMP Exporter
==================================


https://github.com/prometheus/snmp_exporter
https://github.com/prometheus/snmp_exporter/releases



===> Dashboard
    https://grafana.com/grafana/dashboards/11169



===> Prometheus Configuration
scrape_configs:
  - job_name: 'snmp'
    static_configs:
      - targets:
        - 192.168.1.2  # SNMP device.
    metrics_path: /snmp
    params:
      module: [if_mib]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9116  # The SNMP exporter's real hostname:port.