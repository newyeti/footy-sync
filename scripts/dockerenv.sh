#!/bin/bash

if [[ -z "${INFRA}" ]]; then
  echo "Environment variable 'INFRA' is not set."
else 
  credentials=$(echo $INFRA | base64 --decode)
  echo $credentials
  export INFRA=$credentials
fi

if [[ -z "${RAPID_API}" ]]; then
  echo "Environment variable 'INFRA' is not set."
else 
  api_keys=$(echo $RAPID_API | base64 --decode)
  echo $api_keys
  export RAPID_API=$api_keys
fi
