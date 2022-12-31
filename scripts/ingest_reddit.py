import requests
import pandas as pd 

CLIENT_ID = ""#Put it in env var
SECRET_TOKEN = "" 
USERNAME = ""
REDDIT_PASSWORD = ""
#https://docs.google.com/presentation/d/1Mc365IrU8aKYpU7JNqtOi73YRW34o5MwNtNDW8ZosuI/edit#slide=id.gb6bfa0f489_0_378
##https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
def main():
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': USERNAME,
                'password': REDDIT_PASSWORD}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'StreamBot/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value

        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

        res = requests.get("https://oauth.reddit.com/r/news/new",
                   headers=headers)

        df = pd.DataFrame()  # initialize dataframe

        # loop through each post retrieved from GET request
        for post in res.json()['data']['children']:
            # append relevant data to dataframe
            df = df.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score']
            }, ignore_index=True)
        print(df.head())

if __name__ == '__main__':
        main()