from django.contrib.auth.models import User
from django.db import models
from django.forms import forms


def validators_number_phone(value):
    if not value.isdigit():
        raise forms.ValidationError("Номер телефона должен состоять только из цифр")


class Flow(models.Model):
    number = models.IntegerField()
    start = models.DateField(blank=True, default=None)
    end = models.DateField(blank=True, default=None)

    def __str__(self):
        return str(self.number)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    github = models.CharField(max_length=50, help_text="Enter your github")
    number_phone = models.CharField(max_length=11, blank=True, validators=[validators_number_phone])
    password = models.CharField(max_length=50, default=None)
    count_tasks = models.IntegerField(default=0)
    flow = models.ForeignKey(Flow, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__getattribute__('username')


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Series(models.Model):
    user = models.OneToOneField(User, related_name='series', on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, default=None)

    def __str__(self):
        return self.user.__getattribute__('username')

