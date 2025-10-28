# Airflow for remote server

## start container for github action runner
```bash
docker build -f build/Dockerfile -t <image_name>:<tag> .

docker run -d \
  -e GITHUB_URL="" \
  -e GITHUB_TOKEN="" \
  --name github-runner \
  <image name>:<tag>
```