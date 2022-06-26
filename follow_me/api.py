from django.conf import settings
import requests
from requests_oauthlib import OAuth1


client_key = settings.TWITTER_CONSUMER_KEY
client_secret = settings.TWITTER_CONSUMER_SECRET
resource_owner_key = settings.TWITTER_ACCESS_TOKEN
resource_owner_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
                   client_secret=client_secret,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret)

authorizationHeaders = {
    "authorization": f'Bearer {settings.TWITTER_BEARER_TOKEN}'
}


def getBearerToken():
    url = "[https://api.twitter.com/oauth2/token?grant_type=client_credentials](https://api.twitter.com/oauth2/token?grant_type=client_credentials)"
    auth = {
        "user": settings.TWITTER_CONSUMER_KEY,
        "pass": settings.TWITTER_CONSUMER_SECRET,
    }
    res = requests.post(url, auth=auth)
    return res.json()


def getWebhook():
    url = f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/webhooks.json',
    res = requests.get(url[0], headers=authorizationHeaders)
    return res.json()


def createWebhook():
    try: 
        res = requests.post(
            'https://api.twitter.com/1.1/account_activity/all/dev/webhooks.json',
            params={'url': 'https://321f-160-152-34-232.eu.ngrok.io/twitter'},
            auth=oauth
        )
        return res.json()
    except: 
        print("An error occrred")



def deleteWebhook(webhookId):
    url = f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/webhooks/${webhookId}.json',
    res = requests.delete(url[0], auth=oauth)
    return res


def getSubscription():
    try: 
        res = requests.post(
            'https://api.twitter.com/1.1/account_activity/all/dev/subscriptions.json',
            params={'url': 'https://321f-160-152-34-232.eu.ngrok.io/twitter'},
            auth=oauth
        )
        return res.json()
    except: 
        print("An error occrred")


def createSubscription():
    try: 
        res = requests.post(
            'https://api.twitter.com/1.1/account_activity/all/dev/subscriptions.json',
            auth=oauth
        )
        return res.json()
    except: 
        print("An error occrred")


def deleteSubscription(userId):
    url = f'{settings.TWITTER_API_URL}/account_activity/all/${settings.TWITTER_WEBHOOK_ENV}/subscriptions/${userId}.json',
    res = requests.delete(url[0], headers=authorizationHeaders)
    return res.json()


# from django.conf import settings
# import requests

# oauth = {
#   "consumer_key": settings.TWITTER_CONSUMER_KEY,
#   "consumer_secret": settings.TWITTER_CONSUMER_SECRET,
#   "token": settings.TWITTER_ACCESS_TOKEN,
#   "token_secret": settings.TWITTER_ACCESS_TOKEN_SECRET
# }

# authorizationHeaders = {
#   "authorization": f'Bearer {settings.TWITTER_BEARER_TOKEN}'
# }

# def getBearerToken():
#     url = "[https://api.twitter.com/oauth2/token?grant_type=client_credentials](https://api.twitter.com/oauth2/token?grant_type=client_credentials)"
#     auth = {
#       "user": settings.TWITTER_CONSUMER_KEY,
#       "pass": settings.TWITTER_CONSUMER_SECRET,
#     }
#     res = requests.post(url, auth=auth)
#     return res.json()


# def getWebhook():
#     url= f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/webhooks.json',
#     res = requests.get(url[0], headers=authorizationHeaders)
#     return res.json()


# def createWebhook(webhookUrl):
#     url = f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/webhooks.json/?url={webhookUrl}'
#     res = requests.post(url, headers=oauth)
#     return res


# def deleteWebhook(webhookId) :
#     url= f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/webhooks/${webhookId}.json',
#     res = requests.delete(url[0], headers=oauth)
#     return res.json()


# def getSubscription():
#     url = f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/subscriptions.json',
#     res = requests.get(url[0], headers=oauth)
#     return res.json()


# def createSubscription() :
#     url = f'{settings.TWITTER_API_URL}/account_activity/all/{settings.TWITTER_WEBHOOK_ENV}/subscriptions.json'
#     res = requests.post(url[0], headers=oauth)
#     return res.json()


# def deleteSubscription (userId):
#     url = f'{settings.TWITTER_API_URL}/account_activity/all/${settings.TWITTER_WEBHOOK_ENV}/subscriptions/${userId}.json',
#     res = requests.delete(url[0], headers=authorizationHeaders)
#     return res.json()
