#!/bin/sh

notifySuccess() {
    curl -X POST -H 'Content-type: application/json'\
    --data "{\"text": "$SUCCESS_MESSAGE" :"\"rocket:\"}" \
    "$WEBHOOK"
}

notifyFail() {
    curl -X POST -H 'Content-type: application/json'\
    --data "{\"text": "$FAIL_MESSAGE": "\"rotating_light:\"}" \
    "$WEBHOOK"
}

if [[ ! -z "$NO_AUTH" ]]; then
    # Execute API request using previously requested Access Token
    status_code=$(curl -k -X POST --write-out %{http_code} --silent --output /dev/null \
        "$JOB_ENDPOINT")
else 
    # Authenticate with your Auth API using OAuth2 Client credentials flow and get an ACCESS TOKEN
    accessToken=$(curl -H "Authorization: Basic $BASIC_CLIENT_CREDENTIALS" \
    -d grant_type=client_credentials \
    --silent "$OAUTH_TOKEN_ENDPOINT" | jq -r .access_token)

    # Execute API request using previously requested Access Token
    status_code=$(curl -k -H "Authorization: Bearer ${accessToken}" \
        -X POST --write-out %{http_code} --silent --output /dev/null \
        "$JOB_ENDPOINT")
fi

if [[ "$status_code" -ne 200 ]]; then
    if [[ -z $FAIL_MESSAGE ]]; then
          echo "Failed to request $JOB_ENDPOINT"
    else
          echo "$FAIL_MESSAGE"
    fi

#   notifyFail
else
    if [[ -z $FAIL_MESSAGE ]]; then
          echo "Successfully completed request $JOB_ENDPOINT"
    else
          echo "$SUCCESS_MESSAGE"
    fi

#   notifySuccess
fi