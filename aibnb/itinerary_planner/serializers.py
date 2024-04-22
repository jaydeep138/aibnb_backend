from rest_framework.serializers import ModelSerializer

from .models import Preference, Review

class PreferenceSerializer(ModelSerializer):
    class Meta:
        model = Preference
        fields = (
            'id', 'user', 'location', 'budget', 'season', 'date',
            'guests'
        )

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id', 'user', 'itinerary', 'rating', 'review', 'date'
        )