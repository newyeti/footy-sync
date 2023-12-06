#!/bin/bash

. ./scripts/env.sh

current_dir=$(echo $(basename $(pwd)))

if [[ "${current_dir}" != "app" ]]; then
  cd app
fi

python main.py
