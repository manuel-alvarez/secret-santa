from django.test import TestCase, RequestFactory
from django.http import Http404

from participants.models import Participant

from giftees.views import GifteeView


class TestGiftee(TestCase):
    participants = [
        {
            "id": 1,
            "name": "Alice",
            "age": 30,
            "list": None,
            "giftee_id": None,
        },
        {
            "id": 2,
            "name": "Bob",
            "age": 20,
            "list": None,
            "giftee_id": 3,
        },
        {
            "id": 3,
            "name": "Claire",
            "age": 33,
            "list": None,
            "giftee_id": 4,
        },
        {
            "id": 4,
            "name": "Dan",
            "age": 28,
            "list": None,
            "giftee_id": None,
        }
    ]

    def setUp(self):
        for item in self.participants:
            Participant.objects.create(**item)
        self.request = RequestFactory()

    def test_get_assigned_giftee(self):
        """
        Just to check that, if there is a current giftee assigned, this is what is returned
        """
        view = GifteeView(request=self.request, kwargs={"participant_id": 2})  # Bob

        giftee = view.get_object()
        self.assertIsNotNone(giftee)
        self.assertEqual(giftee.id, 3)

    def test_get_single_output(self):
        """
        For Alice, the only option left is Bob, since both Claire and Dan has been assigned
        """
        # Lets try ten times
        for i in range(10):
            view = GifteeView(request=self.request, kwargs={"participant_id": 1})  # Alice

            giftee = view.get_object()
            self.assertIsNotNone(giftee)
            self.assertEqual(giftee.id, 2)  # Only Bob is valid

            participant = Participant.objects.get(pk=1)
            self.assertEqual(participant.giftee_id, giftee.id)

            # If everything is ok, remove it to try it again
            participant.giftee = None
            participant.save()

    def test_get_multiple_outputs(self):
        """
        For Dan, there are two options and both Alice and Bob are valid outputs
        """
        # Lets try ten times. It's supposed that there is little probability of getting always the same output, so we
        # can assume that both values are going to be returned due to the fact that the assignment is random
        results = set()
        for i in range(10):
            view = GifteeView(request=self.request, kwargs={"participant_id": 4})  # Dan

            giftee = view.get_object()
            self.assertIsNotNone(giftee)
            self.assertIn(giftee.id, [1, 2])  # Alice and Bob

            results.add(giftee.id)

            participant = Participant.objects.get(pk=4)
            self.assertEqual(participant.giftee_id, giftee.id)

            # If everything is ok, remove it to try it again
            participant.giftee = None
            participant.save()

        # Now we check that both values have been returned
        self.assertIn(1, results)
        self.assertIn(2, results)

    def test_get_no_output(self):
        """
        If there is only one Participant without giftee, the API cannot assign anybody, so it returns 404.
        """
        # First, block the last option
        participant = Participant.objects.get(pk=4)
        participant.giftee_id = 2
        participant.save()

        view = GifteeView(request=self.request, kwargs={"participant_id": 1})  # Alice
        with self.assertRaises(Http404):
            giftee = view.get_object()
