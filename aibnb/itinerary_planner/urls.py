from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from .views import PreferenceViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'preference', PreferenceViewSet, basename='preference')
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    re_path('^', include(router.urls)),
]