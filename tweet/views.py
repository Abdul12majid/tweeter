from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm, UpdateForm, UpdateUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def home(request):
	if request.user.is_authenticated:
		tweets=Tweet.objects.all().order_by('-created_at')
		form=TweetForm()
		if request.method=='POST':
			form=TweetForm(request.POST or None)
			if form.is_valid():
				tweet=form.save(commit=False)
				tweet.user=request.user
				tweet.save()
		return render(request, 'home.html', {'tweets':tweets, 'form':form})
	else:
		messages.success(request, ('Kindly Login'))
		return render(request, 'login_user.html', {})


def profile_list(request):
	if request.user.is_authenticated:
		all_profile=Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {'all_profile':all_profile})
	else:
		messages.success(request, ('Kindly Login'))
		return render(request, 'login_user.html', {})

def profile(request, pk):
	if request.user.is_authenticated:
		profile=Profile.objects.get(user_id=pk)
		following=int(profile.follows.count())
		current_user='w'
		followers=int(profile.followed_by.count())
		tweets=Tweet.objects.filter(user_id=pk).order_by('-created_at')
		if request.method=='POST':
			current_user_profile=request.user.profile
			action=request.POST['follow']
			if action == 'unfollow':
				current_user_profile.follows.remove(profile)
			elif action == 'follow':
				current_user_profile.follows.add(profile)
			current_user_profile.save()
		return render(request, 'profile.html', {'profile':profile, 'following':following, 'followers':followers, 'tweets':tweets, 'current_user':current_user})

	else:
		messages.success(request, ('Kindly Login'))
		return render(request, 'login_user.html', {})

#def follow()

def my_followers(request, pk):
	if request.user.is_authenticated:
		profile=Profile.objects.get(user_id=pk)
		followers=profile.follows.all()
		return render(request, 'followers.html', {'followers':followers})
	else:
		messages.success(request, ('Kindly Login'))
		return render(request, 'login_user.html', {})

def login_user(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('login successful'))
			return redirect('home')
		else:
			messages.success(request, ('Error logging in'))
			return redirect('login')
	return render(request, 'login.html')


def register_user(request):
	form=SignUpForm()
	if request.method=="POST":
		form=SignUpForm(request.POST or None)
		if form.is_valid():
			form.save()
			username=form.cleaned_data['username']
			password=form.cleaned_data['password1']
			first_name=form.cleaned_data['first_name']
			user=authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, (f'Welcome {first_name}'))
			return redirect('home')
	return render(request, 'register.html', {"form":form})

def update_user(request):
	if request.user.is_authenticated:
		current_user=User.objects.get(id=request.user.id)
		profile_user=Profile.objects.get(user__id=request.user.id)
		user_form=UpdateUserForm(request.POST or None, instance=current_user)
		profile_form=ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			login(request, current_user)
			messages.success(request, ('Info updated'))
			return redirect('home')
		return render(request, 'update_user.html', {"user_form":user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ('You need to login to view this page'))
		return redirect('home')


def logout_user(request):
	logout(request)
	#messages.success(request, (f'You are logged out'))
	return redirect('login')
	

def tweet_like(request, pk):
	if request.user.is_authenticated:
		tweet=get_object_or_404(Tweet, id=pk)
		if tweet.likes.filter(id=request.user.id):
			tweet.likes.remove(request.user)
		else:
			tweet.likes.add(request.user)
		return redirect(request.META.get("HTTP_REFERER"))
	else:
		messages.success(request, ('You need to login to view this page'))
		return redirect('home')


def share_tweet(request, pk):
	tweet=get_object_or_404(Tweet, id=pk)
	if tweet:
		return render(request, 'show_tweet.html', {'tweet':tweet})
	else:
		messages.success(request, ('Error finding Tweet'))
		return redirect('home')

def twitter(request):
	if request.user.is_authenticated:
		tweets=Tweet.objects.all().order_by('-created_at')
		current_user=User.objects.get(id=request.user.id)
		profile_user=Profile.objects.get(user__id=request.user.id)
		all_profile=Profile.objects.exclude(user=request.user)
		if request.method=='POST':
			poster=request.user
			post=request.POST['post']
			post_model=Tweet.objects.create(user=poster, body=post)
			post_model.save()
		return render(request, 'index2.html', {'profile_user':profile_user, 'tweets':tweets, 'all_profile':all_profile})
	else:
		messages.success(request, ('You need to login to view this page'))
		return redirect('login')

def unfollow(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		request.user.profile.follows.remove(profile)
		request.user.profile.save()
		return redirect(request.META.get("HTTP_REFERER"))
	else:
		messages.success('login to unfollow this user')
		return redirect('home')

def follow(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		request.user.profile.follows.add(profile)
		request.user.profile.save()
		return redirect(request.META.get("HTTP_REFERER"))
	else:
		messages.success('login to follow this user')
		return redirect('home')

def followers(request, pk):
	
	if request.user.is_authenticated:
		profile=Profile.objects.get(user_id=pk)
		return render(request, 'followers.html', {'profile':profile})
	else:
		messages.success(request, ('login to see who follows you'))
		return redirect('home')

def following(request, pk):
	if request.user.is_authenticated:
		
		profile=Profile.objects.get(user_id=pk)
		return render(request, 'following.html', {'profile':profile})
		
	else:
		messages.success(request, ('login to see who follows you'))
		return redirect('home')

def delete_tweet(request, pk):
	if request.user.is_authenticated:
		tweet=get_object_or_404(Tweet, id=pk)
		if request.user.username == tweet.user.username:
			tweet.delete()
			messages.success(request, ('Tweet Deleted'))
			return redirect(request.META.get("HTTP_REFERER"))
		else:
			messages.success(request, ('Error..'))
			return redirect('home')
	else:
		messages.success(request, ('login to see who follows you'))
		return redirect('home')

def edit_tweet(request, pk):
	if request.user.is_authenticated:
		tweet=get_object_or_404(Tweet, id=pk)		
		if request.user.username == tweet.user.username:
			form=TweetForm(request.POST or None, instance=tweet)
			if request.method == "POST":
				if form.is_valid():
					tweet=form.save(commit=False)
					tweet.user=request.user
					tweet.save()
					messages.success(request, ('Tweet Updated'))
					return redirect(request.META.get("HTTP_REFERER"))
			else:
				return render(request, 'edit_tweet.html', {'tweet':tweet, 'form':form})
		else:
			messages.success(request, ('Error..'))
			return redirect('home')
	else:
		messages.success(request, ('login to see who edit your tweet'))
		return redirect('home')

def search_tweet(request):
	if request.method=='POST':
		search=request.POST['search']
		searched=Tweet.objects.filter(body__contains=search)
		return render(request, 'search_tweet.html', {'searched':searched, 'search':search})
	else:
		return render(request, 'search_tweet.html', {})


def search_user(request):
	if request.method=='POST':
		search=request.POST['search']
		searched=User.objects.filter(username__contains=search)
		return render(request, 'search_user.html', {'searched':searched, 'search':search})
	else:
		return render(request, 'search_user.html', {})
