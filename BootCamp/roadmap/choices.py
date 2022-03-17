from django.db.models import IntegerChoices


class EventStatus(IntegerChoices):
    start = 0, 'Start'
    ready = 1, 'Ready'
    success = 2, 'Success'
