from django.http import Http404
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from participants.views import ParticipantsMixin


class GifteeView(ParticipantsMixin, RetrieveAPIView):
    lookup_url_kwarg = "participant_id"
    lookup_field = 'pk'

    def get_object(self):
        """
        Giftees API endpoint won't return the Participant with a given giftee id, but the Participant WHO is the giftee
         of the given participant_id.
        If Participant with participant_id hasn't got a giftee already, a new one from the available will be assigned.
        Every Participant belongs to a list (there's a global list, when list is None), and the giftee assigned must be
        from the same list.
        If the system is not able to find a giftee, a 404 error is raised
        :return: an instance from the class queryset
        """

        # The parent's method will give us the participant whose giftee we are searching for
        original_participant = super(GifteeView, self).get_object()

        # First, we need to know if the Participant already has a giftee.
        if original_participant.giftee is not None:
            return original_participant.giftee

        # If not, look for the appropriate one
        queryset = self.filter_queryset(self.get_queryset())

        # Firstly, we need to know who are the current giftees
        giftees = list(queryset.exclude(giftee=None).values_list("giftee", flat=True))

        # Then, the new giftee should not be in the list of giftees and cannot be the participant neither
        # And, of course, it has to be in the same list as the participant
        filter_params = {"list": original_participant.giftee}
        excluded_ids = giftees + [original_participant.id]
        negative_filter = {"id__in": excluded_ids}

        try:
            new_giftee = queryset.filter(**filter_params).exclude(**negative_filter).order_by('?')[0]

            original_participant.giftee = new_giftee
            original_participant.save()
        except IndexError:
            raise Http404

        return new_giftee

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        output = serializer.data  # We can skip this and write it in next line, but we left it for debugging purposes
        return Response(output)
