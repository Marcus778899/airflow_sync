# Airflow for remote server

## start container for github action runner

* create a file name "docker.env"
```env
SSH_USER=
SSH_HOST=
SSH_PASSWORD=
GITHUB_URL=
GITHUB_TOKEN=
```

```bash
docker build -f build/Dockerfile -t <image_name>:<tag> .

docker run -d ^
  --env-file docker.env ^
  -v "%cd%\.ssh:/home/runner/.ssh" ^ # os:windows
  --name github-runner ^
  <image name>:<tag>
```