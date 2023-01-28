<!-- omit in toc -->
# Trend-Tracker

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trend-tracker.streamlit.app/)
[![Build & Test](https://github.com/baptiste-pasquier/trend-tracker/actions/workflows/main.yml/badge.svg)](https://github.com/baptiste-pasquier/trend-tracker/actions/workflows/main.yml)
[![codecov](https://codecov.io/github/baptiste-pasquier/trend-tracker/branch/main/graph/badge.svg)](https://codecov.io/gh/baptiste-pasquier/trend-tracker)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


- [1. Prerequities](#1-prerequities)
- [2. Usage with Docker](#2-usage-with-docker)
- [3. Development](#3-development)
  - [3.1. Installation](#31-installation)
  - [3.2. Usage with CLI](#32-usage-with-cli)


## 1. Prerequities

- Sign-up for a Twitter developer account on this [link](https://developer.twitter.com/en/apply-for-access)
- Create a Bearer Token ([documentation](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens))
- Fill in the field `BEARER_TOKEN` in the `.env` file
- Create a Reddit developed application on this [link](https://www.reddit.com/prefs/apps/) ([documentation](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow))
- Fill in the fields `CLIENT_ID`, `SECRET_TOKEN`, `USERNAME` and `PASSWORD` in the `.env` file
- Install and run Kafka ([documentation](https://kafka.apache.org/quickstart))
- Create a MongoDB database in the [cloud](https://www.mongodb.com/cloud/atlas/register) (free) or install the server ([documentation](https://www.mongodb.com/docs/manual/installation/))
- Fill in the fields `CONNECTION_STRING` in the `.env` file

## 2. Usage with Docker

```bash
docker-compose -f docker-compose.yml up
```

## 3. Development

### 3.1. Installation

1. Clone the repository
```bash
git clone https://github.com/baptiste-pasquier/trend-tracker
```

2. Install the project
- With `poetry` ([installation](https://python-poetry.org/docs/#installation)) :
```bash
poetry install
```
- With `pip` :
```bash
pip install -e .
```

3. Install pre-commit
```bash
pre-commit install
```

### 3.2. Usage with CLI

> **Warning**
> Each script must be run in a separate console

1. Twitter streaming:
```bash
python all_services/ingest_tweets/app.py
```

2. Reddit streaming:
```bash
python all_services/ingest_reddit/app.py
```

3. Data preprocessing:
```bash
python all_services/tsf_data/app.py
```

4. Data clustering:
```bash
python all_services/cluster_data/app.py
```

5. Data storage on MongoDB:
```bash
python all_services/store_data/app.py
```

Real-time visualization:
```bash
streamlit run streamlit_app.py
```
