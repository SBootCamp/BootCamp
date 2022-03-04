from django.contrib.auth.models import User
from django.db import models

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Node(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    about = models.CharField(max_length=150, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    deadline = models.IntegerField(default=7)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=(('0', 'В процессе'), ('1', 'Готово к сдаче'), ('2', 'Сдано')))
    startdate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)
