import tweepy
import time
from tweepy_client import twitter_api
import bot_functions
import qa_model


def execute_bot() -> None:
    """
    main method to prepare model and run the bot
    """
    print("Yani? started..")
    api = twitter_api()
    print("Tweepy Authentication is successful.")
    nlp = qa_model.get_bert_qa_model()
    print("Bert QA Model preparation is successful.")
    while True:
        try:
            bot_functions.bot_run(api=api, model=nlp)
            time.sleep(20)
        except tweepy.TweepError as e:
            print(e)
            print('sleeping...')
            time.sleep(60)
        except StopIteration:
            break


if __name__ == '__main__':
    execute_bot()
