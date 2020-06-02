# Client-Jobs-Simulator

A Simulator for generate dynamic jobs and send requests to public-analysis-api

## Getting Started

### Prerequisites

- python 3.7.3
- pipenv 2018.11.26
- docker 18.09.2
- Postgre 11

### Running Development

Installing Packages & Running

```lan=shell

pipenv --python 3.7
pipenv install --dev

pre-commit install

pipenv run src/app.py
```

### Running Production

1. update the .env file
2. run docker container

```lan=shell
docker-compose up -d
```
