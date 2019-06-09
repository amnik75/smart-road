from rest_framework import serializers
from main.models import Pass,Camera,Road

class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = ('pass_id', 'plate_char', 'plate_num', 'speed', 'hour','minute','longitude','latitude')

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('cam_id','province','sequence','longitude', 'latitude')

class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = ('road_id','province','source','destination')
