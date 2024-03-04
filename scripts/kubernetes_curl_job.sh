#!/bin/sh

no_auth=$NO_AUTH
success_message=$SUCCESS_MESSAGE
failed_message=$FAIL_MESSAGE

# Authorization
no_auth=$NO_AUTH
client_id=$CLIENT_ID
client_secret=$CLIENT_SECRET
auth_domain=$AUTH_DOMAIN
audience=$AUDIENCE

# API
season=$SEASON
leagues=$LEAGUE_IDS
standings_endpoint=$STANDINGS_ENDPOINT
fixture_endpoint=$FIXTURE_ENDPOINT
topscorers_endpoint=$TOP_SCORERS_ENDPOINT
topassists_endpoint=$TOP_ASSISTS_ENDPOINT
topredcards_endpoint=$TOP_RED_CARDS_ENDPOINT
topyellowcards_endpoint=$TOP_YELLOW_CARDS_ENDPOINT

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

callApi() {
    endpoint=$1
    access_token=$2

    if [ ! -z "${no_auth}" ]; then
        status_code=$(curl -k -X POST --write-out %{http_code} --silent --output /dev/null \
            "$endpoint")
    else 
        # Execute API request using previously requested Access Token
        status_code=$(curl -k -H "Authorization: Bearer $access_token" \
            -X POST --write-out %{http_code} --silent --output /dev/null \
            "$endpoint")

        echo "Status code:${status_code}"
    fi

    if [ "${status_code}" -ne 200 ]; then
        if [ -z ${FAIL_MESSAGE} ]; then
            echo "Failed to request $endpoint"
        else
            echo "${FAIL_MESSAGE}"
        fi
    else
        if [ -z ${SUCCESS_MESSAGE} ]; then
            echo "Successfully completed request ${endpoint}"
        else
            echo "$SUCCESS_MESSAGE"
        fi
    fi
}

execute() {
    season=$1
    league=$2
    endpoint=$3
    access_token=$4

    url=$(echo $endpoint | sed -e "s/{season}/${season}/" -e "s/{league}/${league}/")
    callApi $url $access_token
}

echo "#############################"
echo "Staring daily job"
echo "#############################"


# Authenticate with your Auth API using OAuth2 Client credentials flow and get an ACCESS TOKEN
access_token=$(curl -X 'POST' \
    --url "https://$auth_domain/oauth/token" \
    --header "content-type: application/x-www-form-urlencoded" \
    --data grant_type=client_credentials \
    --data client_id=$client_id \
    --data client_secret=$client_secret \
    --data audience=$audience \
    | jq -r .access_token)

echo "access token: $access_token , endpoint:$endpoint"

if [ -z ${access_token} ]; then
    echo "Unable to get access token."
    exit 1
fi

# Save the current value of IFS
OLD_IFS=$IFS

# Set the IFS to comma
IFS=','

# Loop through each value
for league in $leagues; do
    execute $season $league $standings_endpoint $access_token
    execute $season $league $fixture_endpoint $access_token
    execute $season $league $topscorers_endpoint $access_token
    execute $season $league $topassists_endpoint $access_token
    execute $season $league $topredcards_endpoint $access_token
    execute $season $league $topyellowcards_endpoint $access_token
done

# Restore the value of IFS
IFS=$OLD_IFS

echo "#############################"
echo "Finished daily job" echo "#############################"

exit 0