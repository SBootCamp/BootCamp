# Generated by Django 4.0.2 on 2022-03-12 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('about', models.CharField(blank=True, max_length=150)),
                ('deadline', models.IntegerField(default=7)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='roadmap.node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'В процессе'), ('1', 'Готово к сдаче'), ('2', 'Сдано')], max_length=300)),
                ('startdate', models.DateTimeField(auto_now=True)),
                ('enddate', models.DateTimeField(blank=True, default=None, null=True)),
                ('node_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmap.node')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]