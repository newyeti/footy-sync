#!/bin/sh

# source ./scripts/export_vars.sh
source ./scripts/env.sh

cd app

uvicorn main:app --host "0.0.0.0" --port "8000" --reload