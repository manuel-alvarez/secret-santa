from django.conf.urls import url, include
from rest_framework import routers

from secret_santa import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^participants/', include('participants.urls')),
    url(r'^giftees/', include('giftees.urls')),

    url(r'^secret-santa/giftee/(?P<participant_id>\d+)/$', views.GifteeView.as_view(), name='giftee'),
    url(r'^secret-santa/(?P<list_id>\d+)/$', views.SecretSantaListView.as_view(), name='secret_santa_list'),
    url(r'^secret-santa/', views.SecretSantaListView.as_view(), name='default_list'),
]
