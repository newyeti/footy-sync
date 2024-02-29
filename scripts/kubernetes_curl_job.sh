#!/bin/sh

no_auth=$NO_AUTH
success_message=$SUCCESS_MESSAGE
failed_message=$FAIL_MESSAGE
client_credential=$BASIC_CLIENT_CREDENTIALS
oauth_token_endpoint=$OAUTH_TOKEN_ENDPOINT

season=$SEASON
leagues=$LEAGUE_IDS
standings_endpoint=$STANDINGS_ENDPOINT
fixture_endpoint=$FIXTURE_ENDPOINT
topscorers_endpoint=$TOP_SCORERS
topassists_endpoint=$TOP_ASSISTS
topredcards_endpoint=$TOP_RED_CARDS
topyellowcards_endpoint=$TOP_YELLOW_CARDS

leagues=39

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

    if [[ ! -z "${no_auth}" ]]; then
        status_code=$(curl -k -X POST --write-out %{http_code} --silent --output /dev/null \
            "$endpoint")
    else 
        # Authenticate with your Auth API using OAuth2 Client credentials flow and get an ACCESS TOKEN
        access_token=$(curl -X 'POST' \
            --url "https://$AUTH_DOMAIN/oauth/token" \
            --header "content-type: application/x-www-form-urlencoded" \
            --data grant_type=client_credentials \
            --data client_id=$CLIENT_ID \
            --data client_secret=$CLIENT_SECRET \
            --data audience=$AUDIENCE \
            | jq -r .access_token)

        echo "access token: $access_token , endpoing:$endpoint"

        # Execute API request using previously requested Access Token
        status_code=$(curl -H "Authorization: Bearer $access_token" \
            -X POST --write-out %{http_code} --silent --output /dev/null \
            "$endpoint")
    fi

    if [[ "${status_code}" -ne 200 ]]; then
        if [[ -z ${FAIL_MESSAGE} ]]; then
            echo "Failed to request $endpoint"
        else
            echo "${FAIL_MESSAGE}"
        fi

    #   notifyFail
    else
        if [[ -z ${SUCCESS_MESSAGE} ]]; then
            echo "Successfully completed request ${endpoint}"
        else
            echo "$SUCCESS_MESSAGE"
        fi

    #   notifySuccess
    fi
}

execute() {
    season=$1
    league=$2
    endpoint=$3
    url=$(echo $endpoint | sed -e "s/{season}/${season}/" -e "s/{league}/${league}/")
    callApi $url
}

echo "#############################"
echo "Staring daily job"
echo "#############################"

IFS=$IFS,
league_array=()
read -a league_array <<< $leagues

for league in ${league_array[@]}; 
do 
    execute $season $league $standings_endpoint
    # execute $season $league $fixture_endpoint
    # execute $season $league $topscorers_endpoint
    # execute $season $league $topassists_endpoint
    # execute $season $league $topredcards_endpoint
    # execute $season $league $topyellowcards_endpoint
done

echo "#############################"
echo "Finished daily job"
echo "#############################"
