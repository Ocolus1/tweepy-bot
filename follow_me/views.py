from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .config import create_api
import tweepy
import logging
from .models import User, User_list
from django.http import JsonResponse, HttpResponse
import base64
import hashlib
import hmac
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .api import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

oauth_store = {}


# Create your views here.
def index(request):
    # # calling the instance of the consumer
    user_auth = create_api()

    # Making a get request to obtain the athourized url
    authorize_url = user_auth.get_authorization_url(signin_with_twitter=True)

    request_token = user_auth.request_token["oauth_token"]
    request_secret = user_auth.request_token["oauth_token_secret"]

    oauth_store[request_token] = request_secret
    content = {"authorize_url": authorize_url}
    return render(request, "follow_me/index.html", content)


def callback(request):
    verifier = request.GET.get("oauth_verifier")
    oauth_token = request.GET.get("oauth_token")
    if not verifier:
        error_message = "callback param(s) missing"
        content = {
            "erro_message": error_message
        }
        return render(request, 'follow_me/error.html', content)
    if oauth_token not in oauth_store:
        error_message = "oauth_token not found locally"
        content = {
            "erro_message": error_message
        }
        return render(request, 'follow_me/error.html', content)
    request_secret = oauth_store[oauth_token]
    user_auth = create_api()
    user_auth.request_token = {
        "oauth_token": oauth_token,
        "oauth_token_secret": request_secret
    }
    access_token, access_token_secret = (
        user_auth.get_access_token(verifier)
    )
    user_auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(user_auth, wait_on_rate_limit=True)
    id = api.verify_credentials().id_str
    followers = api.get_follower_ids(user_id=id)
    user = api.get_user(user_id=id)
    name = user.name
    screen_name = user.screen_name
    follower_len = user.followers_count
    del oauth_store[oauth_token]
    if User.objects.filter(twitter_id=int(id)).exists():
        prev_user = User.objects.get(twitter_id=int(id))
        ac = prev_user.access_token == access_token
        ac_secret = prev_user.access_token_secret == access_token_secret
        if ac == True and ac_secret == True:
            pass
        else:
            prev_user.access_token = access_token
            prev_user.access_token_secret = access_token_secret
            prev_user.save()

        user = authenticate(twitter_id=int(id), password=access_token)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("An error occured inner")
    else:
        created = User.objects.create_user(
            twitter_id=int(id),
            name=name,
            password=access_token
        )
        if created:
            created.save()
            created.screen_name = screen_name
            created.num_of_followers = follower_len
            created.access_token = access_token
            created.access_token_secret = access_token_secret
            created.save()

            for i in followers:
                User_list.objects.create(user=created, follower=i)

            user = authenticate(twitter_id=int(id), password=access_token)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print("An error occured")
    return redirect("home")


def dashboard(request):
    return render(request, "follow_me/dashboard/dashboard.html")


def dashboard_msg(request):
    print(json.loads(request.body))
    return JsonResponse({"message": "Success"})


@csrf_exempt
def twitter(request):
    if request.method == "GET":
        # creates HMAC SHA-256 hash from incomming token and your consumer secret
        text = request.GET.get("crc_token").encode('utf-8')

        key = bytes(settings.TWITTER_CONSUMER_SECRET, 'utf-8')
        sha256_hash_digest = hmac.new(
            key, msg=text, digestmod=hashlib.sha256).digest()

        # construct response data with base64 encoded hash
        response = {
            'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('utf-8')
        }
        # returns properly formatted json response
        return JsonResponse(response)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            if data['follow_events'] :
                pass
             
        except:
            print("An error occurred")
        return HttpResponse('done')
