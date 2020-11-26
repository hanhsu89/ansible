Deploy Kubernetes Cluster with RKE
==================================

I. Prepare Kubernetes Node to build from RKE
--------------------------------------------
1. **Requirement**

- OS: CentOS 7
- ***Run Provision before run ansible-playbook***
- Information Cluster:
    - RKE: v0.1.15
    - Helm: v2.12.1
    - Kubernetes: v1.12.4
    - Docker: 17.03

- Nginx Ingress: <https://kubernetes.github.io/ingress-nginx/deploy/>
- Nginx Deployment: <https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml>
- Prometheus <https://github.com/rancher/charts/tree/master/charts/prometheus/v6.2.1>
>
2. **Update inventory and variables**

    ```yaml
    demo:
      hosts:
        192.168.10.61:
          roles: rke-node
          hostname: rke-node
          internal_address: 10.10.10.61
          labels: none

        192.168.10.62:
          roles: 
            - controlplane
            - etcd
            - worker
          hostname: rke-01
          internal_address: 10.10.10.62
          labels:
            - 'app: ingress-nginx'

        192.168.10.63:
          roles:
            - controlplane
            - etcd
            - worker
          hostname: rke-02
          internal_address: 10.10.10.63
          labels:
            - 'app: ingress-nginx'

        192.168.10.64:
          roles:
            - controlplane
            - etcd
            - worker
          hostname: rke-03
          internal_address: 10.10.10.64
          labels:
            - 'app: ingress-nginx'

      vars:
        ansible_ssh_port: 1102

        upgrade_os: upgrade

        rke_ssh_user: k8s
        rke_ssh_key: "{{ hostvars['192.168.10.61']['ssh_public_key']['stdout'] }}"

        k8s_cluster_name: lab-k8s
        k8s_max_pods_per_node: 120
        k8s_network_plugin: calico
        k8s_flannel_interface: ens160
        k8s_ingress_rancher: no
        k8s_api_domain:
          - 192.168.10.62
          - 192.168.10.63
          - api.k8s.demo.local
    ```

3. **Update information K8S cluster**

    | Variables           |      Values                              |  Notes                                                           |
    |:-------------------:|:----------------------------------------:|:-----------------------------------------------------------------|
    |roles                |                                          |Roles of nodes                                                    |
    |hostname             |***rke-node***                            |Hostname of nodes                                                 |
    |internal_address     |                                          |IP expose ETCD if server have more 1 network card                 |
    |lables               |                                          |Labels of Nodes                                                   |
    |ansible_ssh_port     |***22***                                  |Port SSH                                                          |
    |upgrade_os           |***upgrade*** / ***no***                  |Upgrade OS if you want                                            |
    |rke_ssh_user         |***k8s***                                 |User SSH to deploy with RKE                                       |
    |rke_ssh_key          |Get from RKE Nodes                        |SSH public key of ***rke_ssh_user***                              |
    |k8s_cluster_name     |***demo-k8s-cluster***                    |Kubernetes domain name                                            |
    |k8s_max_pods_per_node|***120***                                 | Max pods per worker nodes                                        |
    |k8s_network_plugin   |***calico*** / ***canal*** / ***flannel***|Network Plugin                                                    |
    |k8s_flannel_interface|***ens160***                              |Interface use for traffic VXLAN, use with **canal** or **flannel**|
    |k8s_ingress_rancher  |***yes*** / ***no***                      |***yes*** if you want to deploy Rancher Nginx Ingress             |
    |k8s_api_domain       |***api.k8s.demo.local***                  | List IP, Domain of API Kubernetes                                |

4. **Command to setup RKE node**

    ```bash
    ansible-playbook -i after_hosts playbook.yml --limit='example-k8s' --tags=k8s_rke_node
    ```
5. **Command to setup Kubernetes node**

    ```bash
    ansible-playbook -i after_hosts playbook.yml --limit='example-k8s' --tags=k8s_node
    ```
II. Deployment Kubernetes Cluster
---------------------------------

1. SSH to RKE Node , switch to user ***rke_ssh_user***
2. Full Script deployment

   ```bash
   #!/bin/bash

   # Deploy Cluster Kubernetes
   rke up

   # Install helm
   bash tools/helm.sh

   # Deploy ingress-nginx
   kubectl -f tools/ingress-nginx.yaml

   # Deploy Prometheus and Grafana Dashboard
   # Edit domain for prometheus and grafana before run
   # Default domain {grafana,prometheus}.kubernetes.example.com
   helm install -n prometheus tools/prometheus -f tools/prometheus/values.yaml
   ```
3. Notes
- Ingress nginx deploy Daemonset with node lables: ***app=ingress-nginx***
- Prometheus and Grafana run without PersistentVolumeClaim(PVC) so it will lose data if restart pods
- Default Grafana Dashboard User: ***admin / khongcopass***
- Login to Grafana and Import ingress_dashboard.json