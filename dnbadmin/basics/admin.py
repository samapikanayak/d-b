"""
basic model admin
"""
from django.contrib import admin
from basics.models import Timezone, DateFormat, CustomFormFieldType
# Register your models here.

admin.site.register(Timezone)
admin.site.register(DateFormat)
admin.site.register(CustomFormFieldType)
