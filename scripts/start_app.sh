#!/bin/bash

. ./scripts/env.sh

current_dir=$(echo $(basename $(pwd)))

if [[ "${current_dir}" != "app" ]]; then
  cd app
fi

uvicorn main:app --host "0.0.0.0" --port "8000" --reload
