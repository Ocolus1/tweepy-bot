import tweepy
import logging
from django.conf import settings

logger = logging.getLogger()

def create_api():
    """
    This function initialise an instance of the user
    and returns the instance.
    """
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        callback="https://321f-160-152-34-232.eu.ngrok.io/callback"
    )
    return auth
