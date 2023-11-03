## Run app
run:
	./scripts/start_app.sh

dockerbuild:
	docker build -t newyeti/footy-sync-service .

dockerrun:
	docker run -d --name footy-container -p 8000:80 newyeti/footy-sync-service