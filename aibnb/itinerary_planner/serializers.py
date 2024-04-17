from rest_framework.serializers import ModelSerializer

from .models import Preference

class PreferenceSerializer(ModelSerializer):
    class Meta:
        model = Preference
        fields = (
            'id', 'user', 'location', 'budget', 'season', 'date',
            'guests'
        )