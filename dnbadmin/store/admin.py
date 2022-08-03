"""
store model admin
"""
from django.contrib import admin
from store.models import BusinessUnitGroup, BusinessUnit

# Register your models here.
admin.site.register(BusinessUnitGroup)
admin.site.register(BusinessUnit)
