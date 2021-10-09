import re
import tweepy
from bs4 import BeautifulSoup
import requests


def read_last_seen(FILE_NAME: str) -> int:
    """
    gets the id of last seen tweet
    Args:
        FILE_NAME: static file name which stores the last seen id
    Returns:
        last_seen_id: id of the tweet
    """
    file_read = open(FILE_NAME, 'r')
    readed = file_read.read()
    if readed != "":
        last_seen_id = int(readed.strip())
        file_read.close()
        return last_seen_id
    else:
        return 0
    print("Last Seen ID is readed.")


def store_last_seen(FILE_NAME: str, last_seen_id: int) -> None:
    """
    saves the id of a last seen tweet in the txt
    Args:
        FILE_NAME: static file name which stores the last seen id
        last_seen_id: id of the tweet
    """
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    print("Last Seen ID is stored.")
    return


def is_not_reply(tweet):
    count = tweet.full_text.count('@')
    return count < 5


def get_tweet_root(tweet_id: int, api: tweepy.API):
    """
    gets the origin tweet which is mentioned
    Args:
        tweet_id: id of the mention
        api: authenticated tweepy api object
    Returns:
        mentioned root tweet object
    """
    print("Getting Tweet Root..")
    while api.get_status(tweet_id).in_reply_to_status_id is not None:
        tweet_id = api.get_status(tweet_id).in_reply_to_status_id
    return api.get_status(tweet_id, tweet_mode="extended")


def get_clean_tweet(tweet: str) -> str:
    """
    cleans text from urls and words begin with @,#
    Args:
        tweet: text version of tweet
    Returns:
        cleaned text
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9])|(\w+:\/\/\S+)", " ", tweet).split())


def track_url(org_url: str) -> str:
    """
    tracks the url and where it leads to and returns the final redirected url
    Args:
        org_url: link in the root tweet
    Returns:
         redirected url
    """
    print("Tracking URL..")
    url = "https://wheregoes.com/trace/"
    data = {'url': org_url, 'ua': 'Wheregoes.com Redirect Checker/1.0'}
    post_data = requests.post(url, data=data).text
    soup = BeautifulSoup(post_data, 'lxml')
    url_list = soup.find_all('div', class_="cell url")
    redirected_url = url_list[-1].contents[1]['href']
    print("Returning redirected URL..")
    return redirected_url if redirected_url is not "" else ""
