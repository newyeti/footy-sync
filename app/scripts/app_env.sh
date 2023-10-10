#!/bin/sh

mongo_credentials=`gcloud secrets versions access latest --secret=newyeti_mongo_credentials`
bq_credentials=`gcloud secrets versions access latest --secret=newyeti_bq_credentials`
infra_credentials=`gcloud secrets versions access latest --secret=upstash_infra_credentials`

get_credentials() {
    type=$1
    json_key=$2

    if [[ ${type} == "mongo" ]]; then
        echo $( jq -r  $json_key <<< "${mongo_credentials}" )
    elif [[ ${type} == "infra" ]]; then
        echo $( jq -r  $json_key <<< "${infra_credentials}" )
    fi
}


environment=$(echo $APP_ENV)

if [[ -z "${environment}" ]]; then
    environment="dev"
fi

echo "Setting ${environment} envrionment variables"

env_infra="dev"
env_mongo="dev"

if [[ ${environment} == "prod" ]]; then
    env_infra="control_cluster"
    env_mongo="prod"
fi

#Mongo DB
export MONGO_HOSTNAME=$(get_credentials "mongo" ".${env_mongo}.hostname")
export MONGO_USERNAME=$(get_credentials "mongo" ".${env_mongo}.username")
export MONGO_PASSWORD=$(get_credentials "mongo" ".${env_mongo}.password")

#BigQuery
export BIGQUERY_CREDENTIALS=${bq_credentials}

#Redis
export REDIS_HOSTNAME=$(get_credentials "infra" ".${env_infra}.redis.hostname")
export REDIS_PORT=$(get_credentials "infra" ".${env_infra}.redis.port")
export REDIS_PASSWORD=$(get_credentials "infra" ".${env_infra}.redis.password")
export REDIS_SSL_ENABLED=TRUE

#Kafka
export KAFKA_BOOTSTRAP_SERVERS=$(get_credentials "infra" ".${env_infra}.kafka.bootstrap_servers")
export KAFKA_USERNAME=$(get_credentials "infra" ".${env_infra}.kafka.username")
export KAFKA_PASSWORD=$(get_credentials "infra" ".${env_infra}.kafka.password")

echo "Setting environment variables completed."
