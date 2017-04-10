from django.conf.urls import url

from participants import views


urlpatterns = [
    url(r'^$', views.ParticipantsView.as_view(), name="participant-list"),
    url(r'^(?P<pk>\d+)/$', views.ParticipantView.as_view(), name="participant-detail"),
]
