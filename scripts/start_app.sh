#!/bin/sh

source ./scripts/export_vars.sh

cd app

uvicorn main:app --reload