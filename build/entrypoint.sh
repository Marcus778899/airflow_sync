#!/bin/bash
set -e

cd /actions-runner

if [[ -z "${GITHUB_URL}" || -z "${GITHUB_TOKEN}" ]]; then
  echo "❌ Missing GITHUB_URL or GITHUB_TOKEN"
  exit 1
fi

./config.sh --url "${GITHUB_URL}" --token "${GITHUB_TOKEN}" --unattended --replace
exec ./run.sh