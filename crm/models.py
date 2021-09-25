from django.contrib.auth.models import User
from django.contrib.postgres.fields import *
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', related_query_name='user', on_delete=models.CASCADE,
                                primary_key=True)
    name = models.CharField(max_length=100, default='')
    avatar = models.ImageField(upload_to='user_avatars/', blank=True,
                               null=True, default='user_avatars/default.png')
    user_type = models.IntegerField(null=False)  # 0 is emp, 1 is client
    user_position = models.CharField(max_length=40)

    managers = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])
    subordinates = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])

    tasks = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])
    events = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])

    def get_absolute_url(self):
        return reverse("profile", kwargs={"user_id": self.user_id})


class Task(models.Model):
    task_type = models.IntegerField(null=False)
    task_status = models.IntegerField(null=False, default=0)


class Indicator(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(null=True, blank=True)


class Competence(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    indicators = models.ManyToManyField(Indicator())


class Question(models.Model):
    type = models.IntegerField(null=False, blank=True, default=1)
    description = models.CharField(max_length=100, default='')
    competence = models.ForeignKey(Competence, related_name='competence', related_query_name='competence',
                                   on_delete=models.CASCADE, null=True)


class GradeTemplate(models.Model):
    owner = models.ForeignKey(Profile, related_name='owner', related_query_name='owner',
                              on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, default='')
    type = models.IntegerField(null=False)
    questions = models.ManyToManyField(Question())


class Schedule(models.Model):
    grade_template = models.ForeignKey(GradeTemplate, related_name='grade_template',
                                       related_query_name='grade_template',
                                       on_delete=models.CASCADE, null=True)
    owner = models.IntegerField(null=False, blank=True, default=-1)
    subordinate = models.IntegerField(null=False, blank=True, default=-1)
    date_from = models.DateTimeField(null=False)
    date_to = models.DateTimeField(null=False)
    status = models.IntegerField(null=False, default=0)
