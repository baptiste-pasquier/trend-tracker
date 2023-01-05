import requests
import json

def get_headers_reddit(secret_config: dict) -> dict:
    """Function to communicate with the Reddit API and get back the headers to send a request

    Arguments
    ---------
    secret_config : dict
        Configuration file as a Python dictionnary

    Returns
    -------
    dict
        Configuration headers for the API
    """

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(
        secret_config["REDDIT"]["CLIENT_ID"], secret_config["REDDIT"]["SECRET_TOKEN"]
    )

    data = {
        "grant_type": "password",
        "username": secret_config["REDDIT"]["USERNAME"],
        "password": secret_config["REDDIT"]["REDDIT_PASSWORD"],
    }

    headers = {"User-Agent": "StreamBot/0.0.1"}

    # send our request for an OAuth token
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )


    TOKEN = res.json()["access_token"]

    # add authorization to our headers dictionary
    headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}}

    return headers
