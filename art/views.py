import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from art.models import Artwork, ProfilePicture, create_otp, OTP
from .forms import ArtworkEditForm, UserLoginForms, ArtPostCreateForms, UserCreateForms, UserProfileEdit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save


# Create your views here.
def home(request):
    user = User.objects.order_by('?')
    context = {
        'users': user
    }

    return render(request, template_name='index.html', context=context)

def details(request,user):
    user_artworks = Artwork.objects.filter(artist__username=user)
    context = {
        'arts' : user_artworks
    }
    return render(request, template_name='details.html', context=context)

def detail_art(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    context = {
        'arts': artwork
    }
    return render(request, template_name='detail_art.html', context=context)


@login_required(login_url='login')
def edit(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    forms = ArtworkEditForm(instance=artwork)
    if request.method == 'POST':
        forms = ArtworkEditForm(request.POST or None, request.FILES or None, instance=artwork)
        if forms.is_valid():
            forms.save()
            return redirect('details', user=artwork.artist.username)

    context = {
        'form': forms
    }
    return render(request, template_name='edit.html', context=context)

def login_user(request):
    forms = UserLoginForms()
    if request.method == 'POST':
        forms = UserLoginForms(request.POST or None)
        if forms.is_valid():
            user = forms.cleaned_data['username']
            pasw = forms.cleaned_data['password']
            userdata = authenticate(request, username=user, password=pasw)
            if userdata is not None:
                login(request, userdata)
                return redirect('home')
            else:
                return redirect('verify', user=user)
    return render(request, template_name='login.html', context={'forms': forms})


def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def art_post(request):
    forms = ArtPostCreateForms(initial={'artist': request.user})
    if request.method == 'POST':
        forms = ArtPostCreateForms(request.POST or None, request.FILES or None)
        if forms.is_valid():
            forms.save()
            return redirect('details', user=request.user)
    return render(request, template_name='artpost.html', context={'form': forms})

def user_create(request):
    forms = UserCreateForms()
    if request.method == 'POST':
        forms = UserCreateForms(request.POST)
        if forms.is_valid():
            user = forms.save()
            post_save.connect(create_otp, sender=User)
            get_user = User.objects.get(username=user.username)
            get_user.is_active = False
            get_user.save()
            return redirect('login')
    return render(request, template_name='user_create.html', context={'form': forms})

def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, template_name='profile.html', context={'users': user})

def user_profile_edit(request, id):
    user = User.objects.get(id=id)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'avater': user.profile_picture.avater
    }
    forms = UserProfileEdit(initial=data)
    avaterModel = ProfilePicture()
    if request.method == 'POST':
        forms = UserProfileEdit(request.POST or None, request.FILES or None)
        if forms.is_valid():
            fname = forms.cleaned_data['first_name']
            lname = forms.cleaned_data['last_name']
            email = forms.cleaned_data['email']
            avater = forms.cleaned_data['avater']
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.profile_picture.avater = avater
            user.save()
            return redirect('profile', username=user.username)
    return render(request, template_name='edit_profile.html', context={'form': forms})

def verify_user(request, user):
    if request.method == 'POST':
        otp_value = request.POST['otp_filed']
        otp_user = request.POST['username']
        user = User.objects.get(username=otp_user)
        saved_otp_code = OTP.objects.get(user=user).otp_code
        if int(otp_value) == int(saved_otp_code):
            user.is_active = True
            user.save()
            return redirect('login')

    return render(request, template_name='verify.html')