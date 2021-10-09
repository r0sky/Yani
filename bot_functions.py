import transformers
import tweepy
import helper_functions as helper
import article
import qa_model

FILE_NAME = 'last_seen.txt'


def get_news_url(tweet):
    """
    searchs and returns the link in the tweet
    Args:
        tweet: tweet as tweepy object
    Returns:
        url if exists
    """
    print("Searching for URL in the tweet..")
    try:
        return tweet.entities.get('urls')[0].get('expanded_url')
    except:
        print("Url is missing..")
        print("Tweet: {}".format(tweet))
        return None


def reply_tweet(root_tweet, original_mention, api, model):
    """
    method that contains all functions to reply and favourite the mention considered as a question
    Args:
        root_tweet: mentioned root tweet object
        original_mention: mention that triggers Yani
        api: authenticated tweepy api object
        model: pre-trained turkish qa model pipeline
    Returns:
        none
    """
    print("Replying Tweet.")
    print("Original Mention:", original_mention)
    print("Original Mention Text:", original_mention.full_text)
    question = helper.get_clean_tweet(original_mention.full_text)
    print(question)
    news_link = get_news_url(tweet=root_tweet)
    print("news link: {}".format(news_link))
    news_link = helper.track_url(org_url=news_link)
    print("Redirected URL: {}".format(news_link))
    article_content = article.get_news_text(news_url=news_link)
    if article_content is "":
        print("Couldn't get news content!")
    else:
        answer = qa_model.get_answer(news_context=article_content, user_question=question, model=model)
        status = '@' + root_tweet.user.screen_name + " @" + original_mention.user.screen_name + " " + str(answer.get("answer"))
        try:
            api.create_favorite(original_mention.id)
        except:
            pass
        print("Tweet is favorited.")
        api.update_status(status, in_reply_to_status_id=original_mention.id)
        helper.store_last_seen(FILE_NAME, original_mention.id)
        print(status)
        print("Replied!")


def bot_run(api: tweepy.API, model: transformers.pipeline) -> None:
    """
    gets non-replied&mentioned tweets and replies
    Args:
        api: authenticated tweepy api object
        model: pre-trained turkish qa model pipeline
    Returns:
          None
    """
    print("Yani? is running..")
    # gets mentioned tweets which are not already replied
    tweets = api.mentions_timeline(since_id=helper.read_last_seen(FILE_NAME), tweet_mode='extended')
    for tweet in reversed(tweets):
        if helper.is_not_reply(tweet):
            root_tweet = helper.get_tweet_root(tweet_id=tweet.id, api=api)
            reply_tweet(root_tweet=root_tweet, original_mention=tweet, api=api, model=model)
