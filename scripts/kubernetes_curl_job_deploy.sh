#!/bin/sh

kubectl delete job footy-standings-curl-job

# Apply Job
kubectl apply -f ./k8s/footy-chart/jobs/footy-standings-curl-jobs.yaml
