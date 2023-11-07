infra =  $(shell cat ./credentials/infra.json | base64)
rapid_api_keys = $(shell cat ./credentials/rapid_api_keys.json | base64)


## Run app
run:
	./scripts/start_app.sh

dockerbuild:
	docker build -t newyeti/footy-sync-service .

dockerrun:	
	docker run -p 8000:8000 \
	--env "INFRA=${infra}" \
	--env "RAPID_API=${rapid_api_keys}" \
	--name newyeti-container newyeti/footy-sync-service
