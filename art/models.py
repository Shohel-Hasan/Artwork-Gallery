from django.db import models
from django.contrib.auth.models import User
import random, datetime
from .emails import send_mail

# Create your models here.
categories = [
    ('Architecture', "Architecture"),
    ('Ceramics',"Ceramics"),
    ('Conceptual art', 'Conceptual art'),
    ('Drawing', 'Drawing'),
    ('Painting', 'Painting'),
    ('Photography', 'Photography'),
    ('Sculpture', 'Sculpture')
]

class Artwork(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, default='Unknown')
    year = models.DateField(blank=True)
    desc = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=categories, blank=True)
    image = models.ImageField(upload_to='art_image')


    class Meta:
        verbose_name_plural = 'Artwork'

    def __str__(self):
        return self.artist.username + '--' + self.title


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='profile_picture')
    avater = models.ImageField(upload_to='Profile_avater', blank=True)

class OTP(models.Model):

    def get_expired_time():
        return datetime.datetime.now() + datetime.timedelta(minutes=5)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    otp_code = models.CharField(max_length=10, blank=True)
    create_time = models.TimeField(auto_now_add=True)
    expired_time = models.TimeField(default=get_expired_time())


def create_otp(sender, instance, created, **kwargs):
    print('connect')
    generated_otp = random.randint(5000, 10000)
    OTP.objects.create(user=instance, otp_code=generated_otp)
    send_mail(to=[instance.email], otp_code=generated_otp)


