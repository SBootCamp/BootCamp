# Generated by Django 4.0.1 on 2022-02-12 15:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this mentor', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter your name', max_length=100)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this student', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter your name', max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('github', models.CharField(help_text='Enter your github', max_length=50)),
                ('number_telephone', models.IntegerField(max_length=11)),
            ],
        ),
    ]
