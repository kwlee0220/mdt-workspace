#!/bin/bash

minikube start --memory=no-limit --cpus=no-limit
#kubectl -n argo port-forward deployment/argo-server 2746:2746 --address 0.0.0.0

kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=argo:default -n argo
kubectl -n argo get svc argo-server -o yaml
kubectl -n argo port-forward svc/argo-server 2746:2746
