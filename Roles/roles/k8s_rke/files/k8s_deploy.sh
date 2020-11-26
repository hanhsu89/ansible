#!/bin/bash

# Deploy Cluster Kubernetes
echo -e 'Install Kubernetes cluster...!!!'
rke up

cd tools
# Install helm
echo -e 'Install helm...!!!'
bash helm.sh

# Check if exists node with lablel app=ingress-nginx
check=`kubectl get nodes -l app=ingress-nginx`
if [ -z $check ]; then
  echo -e '\nNot found node lables with app=ingress-nginx \nPlease label node before create ingress-nginx...!!!'
else
  # Deploy ingress-nginx
  echo -e '\nInstall Ingress Nginx...!!!'
  kubectl create -f ingress-nginx.yaml

  # Deploy Prometheus and Grafana Dashboard
  echo -e '\nInstall Prometheus and Grafana...!!!'
  tar xf prometheus.tar.gz && rm -rf prometheus.tar.gz
  helm install -n prometheus ./prometheus -f prometheus/values.yaml
  echo -e '\nLink Grafana: http://grafana.kubernetes.example.com'
  echo 'Default User/Pass: admin/khongcopasss'
fi
cd ..