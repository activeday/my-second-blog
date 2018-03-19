from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class common_detail(models.Model):
    #owner = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=30)
    apartment_name = models.CharField(max_length=30)
    apartment_type = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    rent = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    phone = models.IntegerField(default=0)
    location = models.CharField(max_length=30)
    apartment_image = models.ImageField(upload_to='images/%Y/%m/%d/',null=True, blank=True)
    description = models.TextField(blank=True,max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #email_confirmed = models.BooleanField(default=False)


class Document(models.Model):
    owner = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
