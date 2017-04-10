from django.db import models


# Participants will be grouped in lists, so this API can be used by different groups of people
class List(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, unique=True)


class Participant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    list = models.ForeignKey(List, related_name="participants", null=True)  # Every participant belong to a list
    giftee = models.ForeignKey("Participant", null=True, default=None)

    def __str__(self):
        return '%s, %s' % (self.id, self.name)