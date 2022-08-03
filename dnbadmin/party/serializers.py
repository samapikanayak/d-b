from rest_framework import serializers
from party.models import ContactPurposeType,ContactMethodType,ISO3166_1Country,ISO3166_2CountrySubdivision

class ContactPurposeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPurposeType
        fields = '__all__'
    def to_representation(self, instance):
        return {
            'code': instance.CD_TYP_CNCT_PRPS,
            'name': instance.NM_TYP_CNCT_PRPS
        }

class ContactMethodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMethodType
        fields = '__all__'
    def to_representation(self, instance):
        return {
            'code': instance.CD_TYP_CNCT_MTH,
            'name': instance.NM_TYP_CNCT_MTH
        }

class ISO3166_1CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ISO3166_1Country
        fields = ['CD_CY_ISO','NM_CY']
    def to_representation(self, instance):
        return {
            'code': instance.CD_CY_ISO,
            'name': instance.NM_CY
        }
class ISO3166_2CountrySubdivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISO3166_2CountrySubdivision
        fields = ['ID_ISO_3166_2_CY_SBDVN','NM_ISO_CY_PRMRY_SBDVN']
    def to_representation(self, instance):
        return {
            'id': instance.ID_ISO_3166_2_CY_SBDVN,
            'name': instance.NM_ISO_CY_PRMRY_SBDVN
        }
