from django import forms
from .models import Artwork
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ArtworkEditForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Artwork
        fields = '__all__'
        widgets = {'artist': forms.HiddenInput()}


class UserLoginForms(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255,widget=forms.PasswordInput())

class ArtPostCreateForms(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'
        widgets = {'artist': forms.HiddenInput()}

class UserCreateForms(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileEdit(forms.Form):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.CharField(max_length=50, required=False)
    avater = forms.ImageField(required=False)