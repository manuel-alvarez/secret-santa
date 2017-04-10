from django.conf.urls import url

from giftees import views


urlpatterns = [
    url(r'^(?P<participant_id>\d+)/$', views.GifteeView.as_view(), name="giftee-detail"),
]
