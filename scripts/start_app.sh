#!/bin/sh

source ./scripts/export_vars.sh

cd app

uvicorn server:app --host "0.0.0.0" --port "80" --reload