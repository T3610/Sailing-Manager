from rest_framework import serializers
from .models import RaceEvent, Racer, Boat

class BoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boat
        fields = ("BoatName", "PyNumber")

class RacerSerializer(serializers.ModelSerializer):
    Boat = BoatSerializer()

    class Meta:
        model = Racer
        fields = "__all__"

class RaceEventSerializer(serializers.ModelSerializer):
    Racer = RacerSerializer()
    class Meta:
        model = RaceEvent
        fields = "__all__"