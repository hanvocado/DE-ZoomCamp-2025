# Module 1: Basics and Setups

## Docker

A **Docker image** is a _snapshot_ of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

Docker containers are ***stateless***: any changes done inside a container will not be saved when the container is killed and started again. This is an advantage because it allows us to restore any container to its initial state in a reproducible manner.

### Getting started with Docker

👉 Write Dockerfile

👉 Build Docker image:
```bash
docker build -t [image-name] [directory]
```

👉 Run container:
```bash
docker run [image-name] [arg]
```