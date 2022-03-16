# Generated by Django 4.0.2 on 2022-03-11 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import registration.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('start', models.DateField(blank=True, default=None)),
                ('end', models.DateField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(blank=True, default=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='series', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github', models.CharField(help_text='Enter your github', max_length=50)),
                ('number_phone', models.CharField(blank=True, max_length=11, validators=[registration.models.validators_number_phone])),
                ('password', models.CharField(default=None, max_length=50)),
                ('count_tasks', models.IntegerField(default=0)),
                ('flow', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.flow')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
