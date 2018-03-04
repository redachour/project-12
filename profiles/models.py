from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from projects.models import *


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(default='')
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        if self.first_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class ProfileSkill(models.Model):
    name = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile)

    def __str__(self):
        return self.name


class Application(models.Model):
    applicant = models.ForeignKey(User, related_name='application')
    project = models.ForeignKey('projects.Project')
    position = models.ForeignKey('projects.Position',
                                 related_name='applications')
    is_accepted = models.NullBooleanField(default=None)

    def __str__(self):
        return '{} for {}'.format(self.position, self.project)
