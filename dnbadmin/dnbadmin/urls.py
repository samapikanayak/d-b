"""dnbadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    '''swagger scheme generator'''

    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        return schema


SchemaView = get_schema_view(
    openapi.Info(
        title="D&B Supply Api List",
        default_version='v1',
        description="Api description",
        terms_of_service="https://www.dnb.com",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="Tset License"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', SchemaView.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/', include('login_authentication.urls')),
    path('basic/', include('basics.urls')),
    path('global/', include('globalsettings.urls')),
    path('unitofmeasure/', include('unitofmeasure.urls')),
    path('sellingrule/', include('sellingrule.urls')),
    path('depositrule/', include('depositrule.urls')),
    path('store/', include('store.urls')),
    path('businesshours/', include('workerschedule.urls')),
    path('itempricerule/', include('itempricerule.urls')),
    path('posdepartment/', include('pos_department.urls')),
    path('taxonomy/', include('taxonomy.urls')),
    path('department/', include('department.urls')),
    path('operator/', include('operators.urls')),
    path('permission/', include('accesscontrol.urls')),
    path('position/', include('position.urls')),
]
