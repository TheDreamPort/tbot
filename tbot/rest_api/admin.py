from django.contrib import admin
from import_export import resources
from .models import *
import modelclone
from import_export.admin import ImportExportModelAdmin

class ApplianceResource( resources.ModelResource ):
    class Meta:
        model = Appliance

class ApplianceAdmin( ImportExportModelAdmin, modelclone.ClonableModelAdmin  ):
    resource_class = ApplianceResource
    list_display       = ('name', 'ip_address', 'created_at', 'last_callback', 'active')
    list_display_links = ('name',)
    search_fields      = ('name',)
    ordering           = ['name', 'ip_address']    
    list_per_page      = 50

admin.site.register( Appliance, ApplianceAdmin )

class TBotReadingResource( resources.ModelResource ):
    class Meta:
        model = TBotReading

class TBotReadingAdmin( ImportExportModelAdmin, modelclone.ClonableModelAdmin  ):
    resource_class = TBotReadingResource
    list_per_page      = 50

admin.site.register( TBotReading, TBotReadingAdmin )

class FaceResource( resources.ModelResource ):
    class Meta:
        model = Face

class FaceAdmin( ImportExportModelAdmin, modelclone.ClonableModelAdmin  ):
    resource_class = FaceResource
    list_per_page  = 50

admin.site.register( Face, FaceAdmin )
