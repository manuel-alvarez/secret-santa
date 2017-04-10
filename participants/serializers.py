from rest_framework import serializers
from participants.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name', 'age', 'list', 'giftee_name', 'url')
