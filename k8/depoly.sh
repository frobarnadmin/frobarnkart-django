#!/bin/sh

# kubectl delete -f dev
kubectl apply -f dev

# kubectl delete -f prod
kubectl apply -f prod

# kubectl delete -f test
kubectl apply -f test

# kubectl get ingress

sleep 10

kubectl get pods

echo "\n⛵ Successfully Deployed!\n"
