# m2ds_data_stream_project

## Prerequities

- Sign-up for a Twitter developer account on this [link](https://developer.twitter.com/en/apply-for-access)
- Create a Bearer Token ([documentation](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens))
- Fill in the field `BEARER_TOKEN` in the `secret_config.yml` file
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

1. Stream tweets:
```bash
python scripts/ingest_tweets.py
```

2. Preprocess tweets:
```bash
python scripts/tsf_data.py
```

3. Tweet clustering:
```bash
python scripts/cluster_data.py
```

Run 1 + 2 + 3:
```bash
python scripts/run_all.py
```

Real-time visualization:
```bash
streamlit run scripts/viz_cluster.py
```
