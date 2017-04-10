import requests

from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from participants.models import List, Participant


class SecretSantaListView(TemplateView):
    template_name = "secret_santa.html"

    def get(self, request, *args, **kwargs):
        secret_santa_list_id = kwargs.get("list_id", None)

        kwargs["list_id"] = secret_santa_list_id
        if secret_santa_list_id is None:
            kwargs["list_name"] = "Default list"
        else:
            try:
                secret_santa_list = List.objects.get(pk=secret_santa_list_id)
                kwargs["list_name"] = secret_santa_list.name
            except List.DoesNotExist:
                raise Http404

        response = requests.get(
            "http://" + get_current_site(request).domain + '/participants/',
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            kwargs["participants"] = response.json()
        else:
            kwargs["errors"] = ["API: Can't connect with API."]

        return super(SecretSantaListView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        secret_santa_list_id = kwargs.get("list_id", None)

        data = {
            "name": request.POST.get("name"),
            "age": int(request.POST.get("age")),
            "list": secret_santa_list_id
        }
        response = requests.post(
            "http://" + get_current_site(request).domain + '/participants/',
            json=data,
            headers={'Content-Type': 'application/json'}
        )

        errors = []
        if response.status_code != 200:
            errors.append("Participants: participant can't be saved")
        if secret_santa_list_id is None:
            return redirect('default_list')
        else:
            return redirect('secret_santa_list', list_id=secret_santa_list_id)


class GifteeView(TemplateView):
    template_name = "giftee.html"

    def get(self, request, *args, **kwargs):
        participant_id = kwargs.get("participant_id", None)
        errors = []

        # First, we get the participant data. Of course, using our API
        response = requests.get(
            'http://%s/participants/%s/' % (
                get_current_site(request).domain,
                participant_id
            ),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise Http404

        participant = response.json()

        # Then, we get the giftee data
        response = requests.get(
            'http://%s/giftees/%s/' % (
                get_current_site(request).domain,
                participant_id
            ),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            giftee = response.json()

            kwargs["participant"] = participant
            kwargs["giftee"] = giftee

        else:
            errors.append("Cannot find giftee for this participant")

        return super(GifteeView, self).get(request, *args, **kwargs)
