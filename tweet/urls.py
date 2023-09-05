from . import views
from django.urls import path

urlpatterns = [
    path('', views.twitter, name='home'),
    path('profile_list/', views.profile_list, name='profile-list'),
    path('login/', views.login_user, name='login'),
    path('twitter/', views.twitter, name='twitter'),

    path('update_user/', views.update_user, name='update-user'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/<int:pk>', views.profile, name='profile'),

    path('my_followers/<int:pk>', views.my_followers, name='my-followers'),
    path('tweet_like/<int:pk>', views.tweet_like, name='like-tweet'),
    path('share_tweet/<int:pk>', views.share_tweet, name='share-tweet'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),

    path('follow/<int:pk>', views.follow, name='follow'),
    path('followers/<int:pk>', views.followers, name='followers'),
    path('following/<int:pk>', views.following, name='following'),

    path('delete_tweet/<int:pk>', views.delete_tweet, name='delete-tweet'),
    path('edit_tweet/<int:pk>', views.edit_tweet, name='edit-tweet'),
    path('search_tweet/', views.search_tweet, name='search-tweet'),
    path('search_user/', views.search_user, name='search-user'),



]
