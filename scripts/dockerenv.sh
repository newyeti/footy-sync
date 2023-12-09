#!/bin/bash

export AUTH0=$(echo "ewogICJkb21haW4iOiAiZGV2LXRvZG8yMC5hdXRoMC5jb20iLAogICJhcGlfYXVkaWVuY2UiOiAiaHR0cHM6Ly9mb290eS5uZXd5ZXRpLmNvbSIsCiAgImlzc3VlciI6ICJodHRwczovL2Rldi10b2RvMjAuYXV0aDAuY29tLyIsCiAgImFsZ29yaXRobSI6ICJSUzI1NiIKfQo=" | base64 --decode)

if [[ -z "${INFRA}" ]]; then
  echo "Environment variable 'INFRA' is not set."
else 
  credentials=$(echo $INFRA | base64 --decode)
  result=$?
  if [[ $result == 0 ]]; then
    export INFRA=$credentials
  fi
fi

if [[ -z "${RAPID_API}" ]]; then
  echo "Environment variable 'RAPID_API' is not set."
else 
  api_keys=$(echo $RAPID_API | base64 --decode)
  result=$?
  if [[ $result == 0 ]]; then
    export RAPID_API=$api_keys
  fi
fi

