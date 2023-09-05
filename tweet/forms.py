from django import forms
from django.forms import ModelForm
from .models import Tweet, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UpdateUserForm(ModelForm):
	email=forms.EmailField(min_length=10, label="Valid Email", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}))
	first_name=forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name=forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	class Meta:
		model=User
		fields=('username', 'first_name', 'last_name', 'email',)
	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class']='form-control'

class ProfilePicForm(ModelForm):
	profile_image = forms.ImageField(label='Profile picture')
	profile_bio=forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':"Bio"}))
	profile_link=forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Link"}))
	class Meta:
		model=Profile
		fields=('profile_image', 'profile_bio', 'profile_link', )
		#profile_image = forms.ImageField()
		#labels={
		#'profile_image':'Profile Picture',
		#}

class TweetForm(ModelForm):
	body=forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'placeholder':'Add Meep', 'class':'form-control',}),
		label='',)
	class Meta:
		model=Tweet
		exclude=('user', 'likes', )

class SignUpForm(UserCreationForm):
	email=forms.EmailField(min_length=10, label="Valid Email", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}))
	first_name=forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name=forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	

	class Meta:
		model=User
		fields=('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class']='form-control'
		self.fields['password1'].widget.attrs['class']='form-control'
		self.fields['password2'].widget.attrs['class']='form-control'

class UpdateForm(UserCreationForm):
	email=forms.EmailField(min_length=10, label="Valid Email", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}))
	first_name=forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name=forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	

	class Meta:
		model=User
		fields=('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(UpdateForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class']='form-control'
		self.fields['password1'].widget.attrs['class']='form-control'
		self.fields['password2'].widget.attrs['class']='form-control'

