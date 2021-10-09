from os import environ
import tweepy


def twitter_api() -> tweepy.API:
    """
    authenticates twitter API
    Args:
        none
    Returns:
        authenticated tweepy api object
    """
    print("Tweepy Authentication Started..")
    # key and secrets could be kept in an environment
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api
