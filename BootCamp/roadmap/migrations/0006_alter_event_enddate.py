# Generated by Django 4.0.2 on 2022-02-21 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0005_alter_event_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='enddate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
