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
	--name newyeti-container newyeti/footy-sync-service

docker-stop:
	docker stop newyeti-container
	docker rm newyeti-container

compose-build:
	docker-compose build

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down