from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from ..models import Achievement


@receiver(post_save, sender=User)
def handle_new_job(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        Token.generate_key()
        g = Group.objects.get(name='Students')
        achievement = Achievement(name="It starts easy", description="Completed all introductory tasks", user=user)
        achievement.save()
        user.groups.add(g)


# @receiver(post_save, sender=Event)
# def handle_new_event(sender, **kwargs):
#     if kwargs.get('created', False):
#         event = kwargs.get('instance')
#         user = event.user_id
#         node = event.node_id
#         profile = Profile.objects.filter(user=user)
#         if event.status == '2':
#             profile.count_tasks += 1
#             profile.save()
#
#             if Profile.objects.all().filter(count_tasks=1).count() == 1:
#                 achievement = Achievement(name="First Blood", description="The first to pass the task to the mentor ",
#                                           user=user)
#                 achievement.save()
#
#             if node.name == 'Задача с метаклассами':
#                 achievement = Achievement(name="Kojima", description="Solved the task with metaclasses ",
#                                           user=user)
#                 achievement.save()
#
#             if node.name == 'Задача по реализации Nested Sets':
#                 achievement = Achievement(name="Excellence in woodworking",
#                                           description="Solved the task of implementing Nested Sets on PostgreSQL ",
#                                           user=user)
#                 achievement.save()
#
#             if profile.count_tasks == Node.objects.all().count():
#                 achievement = Achievement(name="Completionist",
#                                           description="Successfully passed all tasks to mentors ",
#                                           user=user)
#                 achievement.save()
