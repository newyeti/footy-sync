#!/bin/sh

app_env=$(echo $APP_ENV)
secret_name="footy_cred_dev"

if [[ -z "${app_env}" ]]; then
    app_env="dev"
fi

if [[ "${app_env}" == "prod" ]]; then
    secret_name= "footy_cred"
    infrastructure_cred=`gcloud secrets versions access latest --secret=$secret_name`
    rapid_api_keys=`gcloud secrets versions access latest --secret=rapid-api-keys`
else 
    infrastructure_cred="$(cat ./credentials/infra.json | base64)"
    rapid_api_keys="$(cat ./credentials/rapid_api_keys.json | base64)"
fi

echo "Setting '${app_env}' envrionment variables"

export APP_ENV=${app_env}

export INFRA=$(echo $infrastructure_cred | base64 --decode)
export RAPID_API=$(echo $rapid_api_keys | base64 --decode)
export GOOGLE_CLOUD_PROJECT="newyeti"
export AUTH0=$(echo "ewogICJkb21haW4iOiAiZGV2LXRvZG8yMC5hdXRoMC5jb20iLAogICJhcGlfYXVkaWVuY2UiOiAiaHR0cHM6Ly9mb290eS5uZXd5ZXRpLmNvbSIsCiAgImlzc3VlciI6ICJodHRwczovL2Rldi10b2RvMjAuYXV0aDAuY29tLyIsCiAgImFsZ29yaXRobSI6ICJSUzI1NiIKfQo=" | base64 --decode)

echo "Setting app_env variables completed."
