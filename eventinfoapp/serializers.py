from rest_framework import serializers
from .models import Events,Highlights,ImportantPersons

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'location', 'created_at']

class HighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = '__all__'

class ImportantPersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantPersons
        fields= '__all__'
