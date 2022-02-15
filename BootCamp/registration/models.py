import uuid

from django.db import models
from django.forms import forms


def validators_number_phone(value):
    if not value.isdigit():
        raise forms.ValidationError("Номер телефона должен состоять только из цифр")


class Mentor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this mentor")
    name = models.CharField(max_length=100, help_text="Enter your name")
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'email']


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this student")
    name = models.CharField(max_length=100, help_text="Enter your name")
    email = models.EmailField(max_length=50)
    github = models.CharField(max_length=50, help_text="Enter your github")
    number_phone = models.CharField(max_length=11, blank=True, validators=[validators_number_phone])

    def __str__(self):
        return self.name

    class Meta:
        permissions = (("take_information", "take information"),)
