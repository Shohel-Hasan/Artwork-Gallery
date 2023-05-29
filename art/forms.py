from django import forms
from .models import Artwork, ProfilePicture
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

class UserProfileEdit(forms.ModelForm):
    avater = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        try:
            profile_picture = ProfilePicture.objects.get(user=self.user)
            self.fields['avater'].initial = profile_picture.avater
        except ProfilePicture.DoesNotExist:
            pass

    def save(self, commit=True):
        user = self.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        avater = self.cleaned_data['avater']
        try:
            profile_ = ProfilePicture.objects.get(user=user)
            profile_.avater = avater
            profile_.save()
        except ProfilePicture.DoesNotExist:
            profile_ = ProfilePicture(user=self.user, avater=avater)
            profile_.save()

        return user, profile_




