from django.urls import path
from django.conf import settings

from . import views


urlpatterns = [
	#Leave as empty string for base url
	path('', views.index, name="index"),
	path('callback', views.callback, name="callback"),
	path('dashboard', views.dashboard, name="dashboard"),
	path('subscribe', views.subscribe, name="subscribe"),
	path('twitter', views.twitter, name="twitter"),
	path('logout/',views.user_logout,name='logout'),
	path('dashboard/msg', views.dashboard_msg, name="dashboard_msg"),
]
