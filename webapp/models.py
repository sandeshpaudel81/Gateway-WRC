from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="informantsLogo/", null=True, blank=True)
    fullName = models.CharField(max_length=1024, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    linkInBio = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return '%s' % (self.fullName)

    @property
    def checkIsStaff(self):
        return self.user.is_staff


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Post(models.Model):
    title = models.CharField(max_length=1024, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="postImages/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    usefulLink = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def getUserDetail(self):
        profile = Profile.objects.get(user=self.user)
        detail = {
            'username': self.user.username,
            'id': self.user.id,
            'profile': profile
        }
        return detail

    def datetime(self):
        datetime = self.date_created+timedelta(minutes=345)
        return datetime.strftime("%Y %B %d, %I:%M:%S %p")