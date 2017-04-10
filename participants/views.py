from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from participants.models import Participant
from participants.serializers import ParticipantSerializer


class ParticipantsMixin(object):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = (AllowAny,)


class ParticipantsView(ParticipantsMixin, ListCreateAPIView):
    pass


class ParticipantView(ParticipantsMixin, RetrieveUpdateDestroyAPIView):
    pass
