FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
COPY build/entrypoint.sh /app/entrypoint.sh

# basic tools + dotnet core dependencies
RUN apt-get update && apt-get install -y \
    curl git jq unzip ca-certificates sshpass openssh-client rsync \
    libicu-dev libkrb5-dev libssl-dev libcurl4-openssl-dev zlib1g \
    && rm -rf /var/lib/apt/lists/*

# python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# github actions runner dependencies
RUN mkdir -p /actions-runner && cd /actions-runner \
    && curl -o actions-runner-linux-x64-2.329.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.329.0/actions-runner-linux-x64-2.329.0.tar.gz \
    && tar xzf ./actions-runner-linux-x64-2.329.0.tar.gz \
    && rm -f actions-runner-linux-x64-2.329.0.tar.gz

# create runner user and set ownership
RUN useradd -m runner \
    && mkdir -p /home/runner/.ssh \
    && chown -R runner:runner /actions-runner /app /home/runner/.ssh \
    && chmod 700 /home/runner/.ssh \ 
    && touch /home/runner/.ssh/authorized_keys \
    && chown runner:runner /home/runner/.ssh/authorized_keys \
    && chmod 600 /home/runner/.ssh/authorized_keys

USER runner
WORKDIR /actions-runner

# make entrypoint executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]