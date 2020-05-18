from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField, StringRelatedField, HyperlinkedModelSerializer
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ApplianceSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Appliance
        fields = [  'id',
                    'name', 'owner', 'ip_address', 'created_at', 'active',
                    'last_callback',]
    
    def create( self, validated_data ):
        """
        Fix stuff.
        """

        new_object = Appliance.objects.create(**validated_data)

        return new_object

class TBotReadingSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = TBotReading
        fields = [ 'id', 'appliance', 'timestamp', 'data', 'average_temperature', ]

    
    def create( self, validated_data ):
        """
        Fix stuff.
        """
        new_object = TBotReading.objects.create(**validated_data)

        return new_object

class FaceSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Face
        fields = [ 'id', 'reading', 'image', 'timestamp', ]

    
    def create( self, validated_data ):
        """
        Fix stuff.
        """
        new_object = Face.objects.create(**validated_data)

        return new_object
