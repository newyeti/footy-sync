#!/bin/sh

kubectl delete job footy-standings-curl-job

# Create config for kubernetes_curl_job.sh script
kubectl create configmap kubernetes-curl-job-script \
 --from-file=./scripts/kubernetes_curl_job.sh \
 -o yaml --dry-run=client | kubectl apply -f -

# Apply Job
kubectl apply -f ./k8s/footy-chart/jobs/footy-standings-curl-jobs.yaml