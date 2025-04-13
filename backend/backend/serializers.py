from rest_framework import serializers
from .models import Vqa_predictions


class VqaPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vqa_predictions
        fields = '__all__'