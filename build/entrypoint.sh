#!/bin/bash
set -e

cd /actions-runner

if [ ! -f "${HOME}/.ssh/id_ed25519" ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -N "" -f "${HOME}/.ssh/id_ed25519"
fi

# upload public key to remote server if credentials are provided
if [[ -n "${SSH_USER}" && -n "${SSH_HOST}" && -n "${SSH_PASSWORD}" ]]; then
    echo "Uploading public key to ${SSH_USER}@${SSH_HOST} ..."

    PUB=$(cat "${HOME}/.ssh/id_ed25519.pub")

    ssh-keyscan -H "${SSH_HOST}" >> "${HOME}/.ssh/known_hosts" 2>/dev/null
    chmod 600 "${HOME}/.ssh/known_hosts"

    sshpass -p "${SSH_PASSWORD}" ssh -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} \
        "mkdir -p /home/${SSH_USER}/.ssh && \
         grep -qxF '${PUB}' /home/${SSH_USER}/.ssh/authorized_keys || echo '${PUB}' >> /home/${SSH_USER}/.ssh/authorized_keys" \
        && echo "Public key uploaded successfully" \
        || echo "Public key upload failed (check credentials or permissions)."
fi

if [[ -z "${GITHUB_URL}" || -z "${GITHUB_TOKEN}" ]]; then
  echo "Missing GITHUB_URL or GITHUB_TOKEN"
  exit 1
fi

# check if runner is already configured
if [ -f ".runner" ]; then
  echo "Runner already configured. Skipping config.sh."
else
  echo "Registering GitHub Runner..."
  ./config.sh --url "${GITHUB_URL}" --token "${GITHUB_TOKEN}" --unattended --replace
fi

# remove runner on exit
cleanup() {
  echo "Cleaning up GitHub Runner..."
  ./config.sh remove --unattended --token "${GITHUB_TOKEN}" || true
  exit 0
}

echo "Runner ready. Listening for jobs..."
trap cleanup SIGTERM SIGINT EXIT
exec ./run.sh &
wait $!
cleanup