"""minnow_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from rest_framework import routers, permissions


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.documentation import include_docs_urls

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from knox import views as knox_views
from rest_api.views.views import *

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'appliance', ApplianceViewSet, 'Appliance')
router.register(r'reading', TBotReadingViewSet, 'TBotReading')
router.register(r'face', FaceViewSet, 'Face')


# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/change_text.html
admin.site.site_header = "TBot Administration"
admin.site.site_title = "TBot Admin Portal"
admin.site.index_title = "Welcome to TBot Portal"

"""
urls that are forwarded from nginx:
admin/
api/
auth/
swagger/
static/
"""

auth_url_list = [
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

api_url_list = [
    url('(?P<version>(v1))/', include(router.urls)),
    path('auth/', include(auth_url_list))
]


urlpatterns = [
    path('api/', include(api_url_list)),
]

# Only enable Django admin and DRF auth pages if DEBUG=True
if settings.DEBUG:
    # Also non-prefixed paths
    urlpatterns.insert(1, path('admin/', admin.site.urls))
    auth_url_list.append(
            path('api/',
                include('rest_framework.urls',
                namespace='rest_framework')))

if not settings.IS_PRODUCTION:
    schema_view = get_schema_view(
       openapi.Info(
          title="TBot API",
          default_version='v1',
          description="Test description",
          terms_of_service="https://www.google.com/policies/terms/",
          contact=openapi.Contact(email="minnow@misi.tech"),
          license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),

        re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),

        re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    ]

urlpatterns += staticfiles_urlpatterns()
