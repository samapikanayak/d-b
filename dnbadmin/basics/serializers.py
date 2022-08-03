'''basic serializer'''
from rest_framework import serializers
from basics.models import DateFormat, Timezone, BusinessUnitType, ImageInformation
from party.models import Language, LegalOrganizationType
from django.contrib.auth.models import User


class LanguageListSerializer(serializers.ModelSerializer):
    '''language'''

    class Meta:
        model = Language
        fields = ['ID_LGE', 'NM_LGE']


class DateFormatListSerializer(serializers.ModelSerializer):
    '''DateFormat'''

    class Meta:
        model = DateFormat
        fields = ['ID_BA_DFMT', 'name']


class TimezoneListSerializer(serializers.ModelSerializer):
    '''Timezone'''

    class Meta:
        model = Timezone
        fields = ['ID_BA_TZN', 'gmt_offset', 'country', 'timezone', 'code']


class BusinessUnitTypeSerializer(serializers.ModelSerializer):
    '''Business Unit Type Serializer Class '''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)

    def get_createdby(self, obj):
        '''get created user name'''
        try:
            user = User.objects.get(id=obj.createdby).get_full_name()
        except User.DoesNotExist:
            user = 'AnonymousUser'
        return user

    def get_updatedby(self, obj):
        '''get updated user name'''
        try:
            if obj.updatedby:
                user = User.objects.get(id=obj.updatedby).get_full_name()
            else:
                user = ''
        except User.DoesNotExist:
            user = 'AnonymousUser'
        return user

    class Meta:
        model = BusinessUnitType
        fields = '__all__'


class LegalOrgTypeSerializer(serializers.ModelSerializer):
    '''Legal Organization Type Serializer Class '''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)

    def get_createdby(self, obj):
        '''get created user name'''
        try:
            user = User.objects.get(id=obj.createdby).get_full_name()
        except User.DoesNotExist:
            user = 'AnonymousUser'
        return user

    def get_updatedby(self, obj):
        '''get updated user name'''
        try:
            if obj.updatedby:
                user = User.objects.get(id=obj.updatedby).get_full_name()
            else:
                user = ''
        except User.DoesNotExist:
            user = 'AnonymousUser'
        return user

    class Meta:
        model = LegalOrganizationType
        fields = '__all__'


class ImageInfoSerializer(serializers.ModelSerializer):
    ''' Image Information Serializer Class '''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)

    def get_createdby(self, obj):
        '''get created user name'''
        try:
            user = User.objects.get(id=obj.createdby).get_full_name()
        except User.DoesNotExist:
            user = 'AnonymousUser'
        return user

    def get_updatedby(self, obj):
        '''get updated user name'''
        try:
            if obj.updatedby:
                user = User.objects.get(id=obj.updatedby).get_full_name()
            else:
                user = ''
        except User.DoesNotExist:
            user = 'AnonymousUser'
        return user

    class Meta:
        model = ImageInformation
        fields = '__all__'


class ImageInfoCreateSerializer(serializers.ModelSerializer):
    ''' Image Information Serializer Class '''

    class Meta:
        model = ImageInformation
        fields = '__all__'
