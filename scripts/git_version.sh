#!/bin/bash

GIT_TAG_TYPE="patch"

if [[ "${COMMIT_MESSAGE}" == *"major.version"* ]]; then
  echo "Found major version in commit message"
  GIT_TAG_TYPE="major"
elif [[ "${COMMIT_MESSAGE}" == *"minor.version"* ]]; then
  echo "Found minor version in commit message"
  GIT_TAG_TYPE="minor"
else
  echo "No major/minor version found. Using default tag 'patch'"
  GIT_TAG_TYPE="patch"
fi

echo "Git Tag Type="$GIT_TAG_TYPE
echo "GIT_TAG_TYPE=${GIT_TAG_TYPE}" >> $GITHUB_ENV
exit 0