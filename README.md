# footy-sync

## Setup Python Virtual Environment
```shell
    source venv/bin/activate
```

## Install Loki Driver
```
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```


## Run application
```shell
    uvicorn main:app --hostname localhost --port 8000  --reload
```
