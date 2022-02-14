from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from .models import Student, Mentor

@login_required
def index(request):
    name_st = Student.name
    name_mt = Mentor.name
    email_st = Student.email
    email_mt = Mentor.email
    git = Student.github
    phone = Student.number_phone

    return render(
        request,
        'index.html',
        context={'name_st': name_st, 'name_mt': name_mt,
                 'email_st': email_st, 'email_mt': email_mt,
                 'git': git, 'phone': phone},
    )
