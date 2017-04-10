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

    @property
    def giftee_name(self):
        """
        Instead of showing the id of the giftee, we will show their name
        """
        return self.giftee.name if self.giftee is not None else None

    def __str__(self):
        """
        String representation of the object
        """
        return '%s' % self.name