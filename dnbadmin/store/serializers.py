'''basic serializer'''
from rest_framework import serializers
from store.models import BusinessUnit, BusinessUnitGroup


class BusinessUnitListSerializer(serializers.ModelSerializer):
    '''BusinessUnit List'''
    class Meta:
        model = BusinessUnit
        fields = ['ID_BSN_UN', 'NM_BSN_UN']


class BusinessUnitGroupListSerializer(serializers.ModelSerializer):
    '''BusinessUnitGroup List'''
    class Meta:
        model = BusinessUnitGroup
        fields = ['ID_BSNGP', 'NM_BSNGP']
