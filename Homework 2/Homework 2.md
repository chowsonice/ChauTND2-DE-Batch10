## Ex1: Deploy 1 hoặc nhiều docker container có thể phục vụ chạy airflow, ETL (sử dụng python, pandas...), có khả năng kết nối với datasource, cloud. 
Guideline:
i) Install Docker.
ii) Install python, airflow (prefect, or dagster), selenium, requests, beautifulsoup, AWS or Azure CLI (if it is too easy for you, install pyspark) on a single container, or on different containers (it depends on how you orchestrate and use these services).

## Ex2: Why docker-compose?
### What is docker-compose?
- Docker Compose is a tool for defining and running multi-container Docker applications.
- Allow users to define their application's services using YAML files
- Used to run multiple Docker commands at the same time
- Automates some options passed to `docker run`
- Manage the lifecycle of these containers, handling tasks such as starting, stopping, and scaling them as needed.

### Why do we use docker-compose?
- Instead of having to write repetitive individual Docker commands for each service, Docker Compose allows users to define all configurations in a single YAML file.
- Consistent, easier to reproduce the same setup across different environments and computers 
- Avoid write out so many options every single time you do `docker run`
- Start up many containers at the same time and automatically connect them

## Ex3: How to reduce the size of Docker images, containers?

Keyword: multistaging build.

In a traditional build, all build instructions are executed in sequence, and in a single build container: downloading dependencies, compiling code, and packaging the application. All those layers end up in your final image. This approach works, but it leads to bulky images carrying unnecessary weight and increasing your security risks. This is where multi-stage builds come in.

In a traditional build, all build instructions are executed in sequence and in a single build container, which comprises of downloading dependencies, compiling code, packaging the application. This works, but could result in image with big size, carrying a lot of unnecessary weight.

Multi-stage build means that you divide your build into many stages, each with a specific purposes. Only the necessary files from the previous steps are carried onto the next steps, thus ensures that only the necessary files are carried into the final stage (or the result image).

Multi-stage build is especially beneficial for applications with large build dependencies.

By separating the build environment from the final runtime environment, you can significantly reduce the image size and attack surface.