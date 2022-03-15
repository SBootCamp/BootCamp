from datetime import datetime

from django.contrib.auth.models import Group, User
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Achievement, Profile


@receiver(post_save, sender=User)
def handle_new_job(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        g = Group.objects.get(name='Students')
        Achievement.objects.create(name="It starts easy", description="Completed all introductory tasks", user=user)
        user.groups.add(g)


@receiver(post_save, sender=Event)
def handle_new_event(sender, **kwargs):
    if not kwargs.get('created', False):
        return None
    event = kwargs.get('instance')
    user = event.user_id
    node = event.node_id
    profile = Profile.objects.filter(user=user)
    if event.status == EventStatus.success:
        profile.count_tasks += 1
        profile.save()
        if Profile.objects.all().filter(count_tasks=1).count() == 1:
            Achievement.objects.create(name="First Blood", description="The first to pass the task to the mentor ",
                                       user=user)

        if Profile.objects.all().filter(count_tasks=1).count() == 1:
            Achievement.objects.create(name="First Blood", description="The first to pass the task to the mentor ",
                                       user=user)

        if event.attempt >= Event.objects.all().aggregate(Max('attempt')).get("attempt__max"):
            Achievement.objects.create(name="Teacher's Pet", description="Most trying to pass the material",
                                       user=user)

        if node.name == 'Задача с метаклассами':
            Achievement.objects.create(name="Kojima", description="Solved the task with metaclasses ",
                                       user=user)

        if node.name == 'Задача по реализации Nested Sets':
            Achievement.objects.create(name="Excellence in woodworking",
                                       description="Solved the task of implementing Nested Sets on PostgreSQL ",
                                       user=user)

        if profile.count_tasks == Node.objects.all().count():
            Achievement.objects.create(name="Completionist",
                                       description="Successfully passed all tasks to mentors ",
                                       user=user)

        series = Series.objects.get(user=user)
        if event.end_day - event.start_day <= node.deadline:
            if series:
                if datetime.now() - series.date_time >= 30:
                    Achievement.objects.create(name="Good Boy", description="At least a month on schedule ",
                                               user=user)
            else:
                series = Series(user=user, date_time=event.start_day)
                series.save()
        elif series:
            series.delete()
