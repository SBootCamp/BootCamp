from django.contrib.auth.models import Group, User
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime

from ..models import Achievement, Profile


@receiver(post_save, sender=User)
def handle_new_job(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        Token.generate_key()
        g = Group.objects.get(name='Students')
        achievement = Achievement(name="It starts easy", description="Completed all introductory tasks", user=user)
        achievement.save()
        user.groups.add(g)


#
# @receiver(post_save, sender=Profile)
# def handle_new(sender, **kwargs):
#     if kwargs.get('created', False):
#         profile = kwargs.get('instance')
#         a = Profile.objects.all().aggregate(Max('count_tasks'))
#         print(a.get("count_tasks__max"))
#         print(Profile.objects.all().filter(count_tasks=a.get("count_tasks__max")))


@receiver(post_save, sender=Event)
def handle_new_event(sender, **kwargs):
    if kwargs.get('created', False):
        event = kwargs.get('instance')
        user = event.user_id
        node = event.node_id
        profile = Profile.objects.filter(user=user)
        if event.status == '2':
            profile.count_tasks += 1
            profile.save()

            if Profile.objects.all().filter(count_tasks=1).count() == 1:
                achievement = Achievement(name="First Blood", description="The first to pass the task to the mentor ",
                                          user=user)
                achievement.save()

            if event.attempt >= Event.objects.all().aggregate(Max('attempt')).get("attempt__max"):
                achievement = Achievement(name="Teacher's Pet", description="Most trying to pass the material",
                                          user=user)
                achievement.save()

            if node.name == 'Задача с метаклассами':
                achievement = Achievement(name="Kojima", description="Solved the task with metaclasses ",
                                          user=user)
                achievement.save()

            if node.name == 'Задача по реализации Nested Sets':
                achievement = Achievement(name="Excellence in woodworking",
                                          description="Solved the task of implementing Nested Sets on PostgreSQL ",
                                          user=user)
                achievement.save()

            if profile.count_tasks == Node.objects.all().count():
                achievement = Achievement(name="Completionist",
                                          description="Successfully passed all tasks to mentors ",
                                          user=user)
                achievement.save()

            series = Series.objects.get(user=user)
            if event.end_day - event.start_day <= node.deadline:
                if series:
                    if datetime.now() - series.date_time >= 30:
                        achievement = Achievement(name="Good Boy", description="At least a month on schedule ",
                                                  user=user)
                        achievement.save()
                else:
                    series = Series(user=user, date_time=event.start_day)
                    series.save()
            elif series:
                series.delete()
