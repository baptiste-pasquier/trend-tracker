# m2ds_data_stream_project

## Prerequities

- Sign-up for a Twitter developer account on this [link](https://developer.twitter.com/en/apply-for-access)
- Create a Bearer Token ([documentation](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens))
- Set the environment variable `TWITTER_BEARER_TOKEN` with your Bearer Token
- Install and run Kafka ([documentation](https://kafka.apache.org/quickstart))

## Installation

Clone the repository and run inside :

- With `poetry` ([installation](https://python-poetry.org/docs/#installation)) :
```bash
poetry install
```

- With `pip` :
```bash
pip install -e .
```

## Usage

> **Warning**
> Each script must be run in a separate console

Stream tweets:
```bash
python scripts/ingest_tweets.py
```
