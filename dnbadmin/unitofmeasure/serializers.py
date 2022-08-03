''' Unit Of Measure Serializer '''
from django.contrib.auth.models import User
import logging
from rest_framework import serializers
from .models import UnitOfMeasure, UnitOfMeasureConversion


logger = logging.getLogger(__name__)


class UomSerializerGet(serializers.ModelSerializer):
    ''' Unit Of Measure Serializer '''
    # createdby = serializers.SerializerMethodField(read_only=True)

    # def get_createdby(self, obj):
    #     '''get created user name'''
    #     try:
    #         user = User.objects.get(id=obj.createdby).get_full_name()
    #     except User.DoesNotExist:
    #         user = 'AnonymousUser'
    #     return user

    class Meta:
        ''' This is a Meta Class'''
        model = UnitOfMeasure
        fields = '__all__'


class UomConvSerializer(serializers.ModelSerializer):
    ''' Unit Of Measure Conversion Serializer '''

    class Meta:
        ''' This is a Meta Class '''
        model = UnitOfMeasureConversion
        fields = '__all__'


class UomCreateSerializer(serializers.ModelSerializer):
    ''' Unit Of Measure Serializer '''
    uom_conversion = UomConvSerializer(many=True)

    class Meta:
        ''' This is a Meta Class'''
        model = UnitOfMeasure
        fields = '__all__'

    def create(self, validated_data):
        uom_conv = validated_data.pop('uom_conversion')
        uom_instance = UnitOfMeasure.objects.get_or_create(**validated_data)
        logger.info("UOM Instance : %s", uom_instance)
        logger.info("UOM Instance Response : %s", uom_instance[0])
        if uom_instance[1]:
            if len(uom_conv) > 0:
                for uom in uom_conv:
                    uom['ID_CVN_UOM_FM'] = uom_instance[0]
                    UnitOfMeasureConversion.objects.create(**uom)
            else:
                logger.info("No Uom Conversion Found")

        else:
            logger.info("Unit Already Exists")
        return uom_instance


class UomUpdateSerializer(serializers.ModelSerializer):
    ''' Unit Of Measure Update Serializer '''
    uom_conversion = UomConvSerializer(many=True)

    class Meta:
        ''' This is a Meta Class'''
        model = UnitOfMeasure
        fields = ['FL_UOM_ENG_MC', 'CD_UOM', 'TY_UOM',
                  'NM_UOM', 'DE_UOM', 'STATUS_UOM', 'uom_conversion']


class UomStatusSerializer(serializers.ModelSerializer):
    '''unit of measure status serializer'''

    def update(self, instance, validated_data):
        instance.STATUS_UOM = validated_data.get(
            'STATUS_UOM', instance.STATUS_UOM)
        instance.save()
        return instance

    class Meta:
        ''' This is a Meta Class'''
        model = UnitOfMeasure
        fields = ["STATUS_UOM"]
