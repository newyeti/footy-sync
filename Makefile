infra =  $(shell cat ./credentials/infra.json | base64)
rapid_api_keys = $(shell cat ./credentials/rapid_api_keys.json | base64)


## Run app
run:
	./scripts/start_app.sh

docker-build:
	docker build -t newyeti/footy-sync-service .

docker-run:	
	docker run -p 8000:8000 \
	--env "APP_ENV=dev" \
	--env "INFRA=${infra}" \
	--env "RAPID_API=${rapid_api_keys}" \
	--name newyeti-container iad.ocir.io/id2dt013po6d/newyeti/footy-sync:v1.0.3

docker-stop:
	docker stop newyeti-container
	docker rm newyeti-container

compose-build:
	docker-compose build

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

nginx:
	docker build -t nginx-proxy infra/nginx/.
	docker tag nginx-proxy iad.ocir.io/id2dt013po6d/infra/nginx-proxy:$(version)
	docker push iad.ocir.io/id2dt013po6d/infra/nginx-proxy:$(version)

grafana:
	docker build -t grafana infra/grafana/.
	docker tag nginx-proxy iad.ocir.io/id2dt013po6d/infra/grafana:$(version)
	docker push iad.ocir.io/id2dt013po6d/infra/grafana:$(version)

footy-sync:
	docker build -t footy-sync .
	docker tag footy-sync iad.ocir.io/id2dt013po6d/newyeti/footy-sync:$(version)
	docker push iad.ocir.io/id2dt013po6d/newyeti/footy-sync:$(version)

footy-sync-amd:
	docker buildx build --platform=linux/amd64 -t footy-sync .
	docker tag footy-sync iad.ocir.io/id2dt013po6d/newyeti/footy-sync:$(version)-amd
	docker push iad.ocir.io/id2dt013po6d/newyeti/footy-sync:$(version)-amd

kube-deploy:
	kubectl -n footy apply -f k8s/deployments.yaml

kube-service:
	kubectl -n footy apply -f k8s/services.yaml

ingress:
	kubectl -n footy apply -f k8s/footy-chart/service-ingress.yaml

secret:
	kubectl -n footy apply -f k8s/footy-chart/secrets/footy-secrets.yaml

configmap:
	kubectl -n footy apply -f k8s/footy-chart/configmaps/footy-configmaps.yaml
	kubectl -n footy apply -f k8s/footy-chart/configmaps/footy-daily-jobs-configmaps.yaml

job-script-configmap:
	kubectl -n footy create configmap kubernetes-curl-job-script \
		--from-file=./scripts/kubernetes_curl_job.sh \
		-o yaml --dry-run=client | kubectl apply -f -

daily-jobs:
	./scripts/kubernetes_curl_job_deploy.sh

helm-grafana:
	helm -n footy upgrade --install grafana grafana/grafana -f k8s/footy-chart/grafana-values.yaml

helm-footy-sync:
	helm upgrade --install footy-sync k8s/footy-chart --namespace footy -f k8s/footy-chart/footy-sync-values.yaml

helm-loki-stack:
	helm upgrade --install loki-stack grafana/loki-stack --namespace footy  -f k8s/footy-chart/loki-stack-values.yaml

helm-tempo:
	helm upgrade --install tempo grafana/tempo --namespace footy 

helm-ingress-nginx:
	helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx -f k8s/footy-chart/nginx-values.yaml --namespace footy

helm-prometheus:
	helm upgrade --install prometheus prometheus-community/prometheus --set alertmanager.enabled=false --namespace footy -f k8s/footy-chart/prometheus-values.yaml

kubernetes-dashboard:
	kubectl apply -f k8s/dashboard/dashboard-adminuser.yaml
	kubectl apply -f k8s/dashboard/cluster-rolebinding.yaml
	kubectl apply -f k8s/dashboard/dashboard-secret.yaml

kubernetes-dashboard-token:
	kubectl -n kubernetes-dashboard create token admin-user

kubernetes-dashboard-secret:
	kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d

kubernetes-dashboard-start:
	kubectl proxy
#http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/.

create-secret:
	kubectl create secret tls footy-newyeti-tls-secret \
--key ./credentials/key.pem \
--cert ./credentials/cert.pem \
--namespace footy


