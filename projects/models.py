from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    requirements = models.TextField(default='')
    timeline = models.CharField(max_length=255, blank=True)
    creator = models.ForeignKey(User, related_name='projects')

    @property
    def open_positions(self):
        return self.positions.exclude(applications__is_accepted=True)

    def __str__(self):
        return self.title


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, related_name='positions')
    skills = models.ManyToManyField(Skill)
    length = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name
