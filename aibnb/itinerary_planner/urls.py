from django.conf.urls import include, re_path
from rest_framework.routers import DefaultRouter
from .views import PreferenceViewSet


router = DefaultRouter()
router.register(r'preference', PreferenceViewSet, base_name='preference')

urlpatterns = [
    re_path('^', include(router.urls)),
]