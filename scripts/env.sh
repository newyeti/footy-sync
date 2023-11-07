#!/bin/sh

app_env=$(echo $APP_ENV)
secret_name="footy_cred_dev"

if [[ -z "${app_env}" ]]; then
    app_env="dev"
fi

if [[ "${app_env}" == "prod" ]]; then
    secret_name= "footy_cred"
fi

echo "Setting '${app_env}' envrionment variables"

export APP_ENV=${app_env}

infrastructure_cred=`gcloud secrets versions access latest --secret=footy_cred_dev`
rapid_api_keys=`gcloud secrets versions access latest --secret=rapid-api-keys`

export INFRA=$(echo $infrastructure_cred | base64 --decode)
export RAPID_API=$(echo $rapid_api_keys | base64 --decode)

echo "Setting app_env variables completed."
