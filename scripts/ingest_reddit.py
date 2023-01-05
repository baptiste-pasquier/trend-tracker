import pandas as pd
import requests

from m2ds_data_stream_project.tools import load_config
from m2ds_data_stream_project.ingest_reddit import get_headers_reddit

# https://docs.google.com/presentation/d/1Mc365IrU8aKYpU7JNqtOi73YRW34o5MwNtNDW8ZosuI/edit#slide=id.gb6bfa0f489_0_378
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c


def main():
    # Load config
    secret_config = load_config("secret_config.yml")

    #Load Headers of requests
    headers = get_headers_reddit(secret_config) 
    #New reddit posts 
    res = requests.get("https://oauth.reddit.com/r/news/new", headers=headers)

    list_df = []
    # loop through each post retrieved from GET request
    for post in res.json()["data"]["children"]:
        list_df.append(
            {
                "subreddit": post["data"]["subreddit"],
                "title": post["data"]["title"],
                "selftext": post["data"]["selftext"],
                "upvote_ratio": post["data"]["upvote_ratio"],
                "ups": post["data"]["ups"],
                "downs": post["data"]["downs"],
                "score": post["data"]["score"],
            }
        )
    df = pd.DataFrame(list_df)
    print(df.head())


if __name__ == "__main__":
    main()
