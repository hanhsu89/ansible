#!/bin/bash

# Create file config

if [ -d ~/.kube ]; then
  mv ~/.kube ~/kube_backup
  mkdir -p ~/.kube
else
  mkdir -p ~/.kube
fi

cp ../kube_config_cluster.yml ~/.kube/config

# Install Helm

kubectl -n kube-system create serviceaccount tiller

kubectl create clusterrolebinding tiller \
  --clusterrole cluster-admin \
  --serviceaccount=kube-system:tiller

helm init --service-account tiller

kubectl -n kube-system  rollout status deploy/tiller-deploy