from django.conf.urls import url, include
from rest_framework import routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^participants/', include('participants.urls')),
    url(r'^giftees/', include('giftees.urls')),
]
