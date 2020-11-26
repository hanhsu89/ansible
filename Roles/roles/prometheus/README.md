Prometheus
=========

Setup Prometheus service, should be setup together with Alertmanager in stand alone mode


https://github.com/markuslindenberg/dashboards


===> Exporter
https://prometheus.io/docs/instrumenting/exporters/
https://github.com/prometheus


===> Packages for prometheus-node-exporter-lua
https://repology.org/project/prometheus-node-exporter-lua/packages
--------------


3 variables for this role:

* PROMETHEUS_VERSION: {{ version }}
* RETENTION_TIME: "90d"
* CONSUL_SERVER: {{ server_ip }}
* ALERTMANAGER_SERVER: {{ server_ip }}
* THANOS_TEAM: "cloudcraft-devops"
* THANOS_ENV: {{ env }}
* THANOS_REPLICA_TAG: {{ tag_for_deduplication }}


#===
https://github.com/prometheus/prometheus/releases
https://prometheus.io/docs/prometheus/latest/configuration/configuration/#configuration-file