from rest_framework import serializers
from .models import Events,Highlights,ImportantPersons, Teams


class HighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = '__all__'

class ImportantPersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantPersons
        fields= '__all__'

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Teams
        fields = '__all__'

    def get_members(self, obj):
        return obj.get_members_list()

class EventSerializer(serializers.ModelSerializer):
    team_spot_1 = serializers.StringRelatedField()
    team_spot_2 = serializers.StringRelatedField()
    team_spot_3 = serializers.StringRelatedField()
    team_spot_4 = serializers.StringRelatedField()
    team_spot_5 = serializers.StringRelatedField()

    class Meta:
        model = Events
        fields = ['id', 'name','description','location' ,'start_date','team_spot_1', 'team_spot_2', 'team_spot_3', 'team_spot_4', 'team_spot_5','image_url']
