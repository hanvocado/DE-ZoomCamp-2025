# Module 2: Workflow Orchestration

#### Contents
* [Orchestration](orchestration)
* [Kestra](kestra)
  - [Start Kestra with a PostgreSQL database backend using Docker Compose](start-kestra-with-a-postgresql-database-backend-using-docker-compose)
* [Create an ETL pipelines](create-an-etl-pipelines)


## 2.1. Orchestration
We can say that an orchestrator is like an orchestra where several different instruments need to come together in unison. In the case of an orchestrator, instead of instruments, *we have different tasks, services, applications, and data pipelines that need to work together harmoniously*. *An orchestrator helps coordinate and manage these various components*, ensuring they execute in the right order, handle dependencies, and maintain proper data flow between them. It provides a centralized way to control and monitor complex workflows that span multiple systems and processes.

Use Cases: Data driven environments, CI/CD pipelines, Distributed systems, Provision resources

## 2.2. Kestra

> Kestra is an open-source orchestrator designed to bring Infrastructure as Code (IaC) best practices to all workflows — from those orchestrating mission-critical applications, IT operations, business processes, and data pipelines, to simple Zapier-style automations.

We can implement it in *no code, low code, or full code*

### Start Kestra with a PostgreSQL database backend using Docker Compose

* Download docker-compose.yml file

```bash
curl -o docker-compose.yml \
https://raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml
```

* The first part in the docker-compose file is

```docker
volumes:
  postgres-data:
    driver: local
  kestra-data:
    driver: local
```

`postgres-data` and `kestra-data` are **named volumes**. These are persistent storage locations managed by Docker.

`driver:local` means that Docker manages storage on the host machine

* Add *pgadmin* service to [docker-compose](docker-compose.yml) file

* Run containers

```bash
docker-compose build
docker-compose up
```

## 2.3. Create an ETL pipelines