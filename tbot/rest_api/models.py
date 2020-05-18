from django.db import models
from django.contrib.auth.models import User  # added
import math, jsonfield, uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from knox.models import AuthToken

@receiver( post_save, sender=settings.AUTH_USER_MODEL )
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        AuthToken.objects.create( instance )

class Appliance( models.Model ):
    name = models.CharField( max_length=24 )
    owner = models.ForeignKey( User, related_name="appliances", on_delete=models.CASCADE )  #added
    ip_address = models.GenericIPAddressField( blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    last_callback = models.DateTimeField( blank=True, null=True )
    active = models.BooleanField(default = True)

    def __str__(self):
        """String for representing the CASEAssessmentTemplate object."""
        return self.name

class TBotReading( models.Model ):
    appliance   = models.ForeignKey( Appliance, related_name="readings", on_delete=models.CASCADE, blank=True, null=True )  #added
    timestamp   = models.DateTimeField( auto_now_add=True )
    data        = jsonfield.JSONField( null=True )
    average_temperature = models.FloatField( default=0.0) 
    
    def __str__( self ):
        """String for representing the CASEAssessmentTemplate object."""
        return self.appliance.name + ":" + self.appliance.ip_address

class Face( models.Model ):
    reading   = models.ForeignKey( TBotReading, related_name="associated_faces", on_delete=models.CASCADE )  #added
    image     = models.BinaryField( blank = True )
    timestamp = models.DateTimeField( auto_now_add=True )
