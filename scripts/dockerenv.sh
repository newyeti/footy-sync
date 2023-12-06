#!/bin/bash

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
