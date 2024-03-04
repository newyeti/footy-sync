#!/bin/sh

kubectl -n footy delete cronjob footy-standings-curl-job

# Apply Job
kubectl -n footy apply -f ./k8s/footy-chart/jobs/footy-daily-curl-jobs.yaml
