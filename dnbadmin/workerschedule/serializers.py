'''work schedule serializer'''
import logging
from pickle import TRUE
from django.contrib.auth.models import User
from rest_framework import serializers
from workerschedule.models import TimeGroup, TimePeriod, TimeGroupTimePeriod
from unitofmeasure.models import UnitOfMeasure
from unitofmeasure.serializers import UomSerializerGet
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class TimePeriodSerializer(serializers.ModelSerializer):
    '''Time Period Serializer'''
    TM_END = serializers.TimeField(
        required=True, help_text="EndTime")

    class Meta:
        model = TimePeriod
        fields = ["status", "NM_PD_TM",
                  "WD", "TM_SRT", "TM_END", "SI_DRN"]


class TimeGroupTimePeriodSerializer(serializers.ModelSerializer):
    '''TimeGroup TimePeriod Serializer'''
    status = serializers.SerializerMethodField(read_only=True)
    NM_PD_TM = serializers.SerializerMethodField(read_only=True)
    WD = serializers.SerializerMethodField(read_only=True)
    TM_SRT = serializers.SerializerMethodField(read_only=True)
    TM_END = serializers.SerializerMethodField(read_only=True)
    SI_DRN = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        '''method to get status timeperiod'''
        return obj.ID_PD_TM.status

    def get_NM_PD_TM(self, obj):
        '''method to get NM_PD_TM timeperiod'''
        return obj.ID_PD_TM.NM_PD_TM

    def get_WD(self, obj):
        '''method to get WD timeperiod'''
        return obj.ID_PD_TM.WD

    def get_TM_SRT(self, obj):
        '''method to get TM_SRT timeperiod'''
        return obj.ID_PD_TM.TM_SRT

    def get_TM_END(self, obj):
        '''method to get TM_END timeperiod'''
        return obj.ID_PD_TM.TM_END

    def get_SI_DRN(self, obj):
        '''method to get SI_DRN timeperiod'''
        return obj.ID_PD_TM.SI_DRN

    class Meta:
        model = TimeGroupTimePeriod
        fields = ["ID_PD_TM", "status", "NM_PD_TM",
                  "WD", "TM_SRT", "TM_END", "SI_DRN"]


class TimeGroupCreateSerializer(serializers.ModelSerializer):
    '''create update serializer'''
    NM_GP_TM = serializers.CharField(
        max_length=40, required=True, help_text="Title")
    uom = serializers.CharField(
        write_only=True, max_length=200, required=TRUE, help_text="Duration UOM Id")
    time_period = TimePeriodSerializer(many=True, write_only=True)

    def create(self, validated_data):
        time_period_data = validated_data.pop('time_period')
        uom_data = validated_data.pop('uom')
        uom_instance = get_object_or_404(UnitOfMeasure, ID_UOM=uom_data)
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        timegroup_instance = TimeGroup.objects.create(**validated_data)
        logger.info("Work Schedule Instance Create: %s", timegroup_instance)
        for time_period in time_period_data:
            time_period['LU_UOM_DRN'] = uom_instance
            time_period_instance = TimePeriod.objects.create(**time_period)
            timegroup_time_period = TimeGroupTimePeriod(
                ID_PD_TM=time_period_instance, ID_GP_TM=timegroup_instance)
            timegroup_time_period.save()
        return timegroup_instance

    def update(self, instance, validated_data):
        time_period_data = validated_data.pop('time_period')
        uom_data = validated_data.pop('uom')
        uom_instance = get_object_or_404(UnitOfMeasure, ID_UOM=uom_data)
        request = self.context['request']
        current_user = request.user
        instance.NM_GP_TM = validated_data.get('NM_GP_TM', instance.NM_GP_TM)
        instance.DE_GP_TM = validated_data.get('DE_GP_TM', instance.DE_GP_TM)
        instance.updatedby = current_user.id
        instance.save()
        logger.info("Work Schedule Instance Update: %s", instance)
        for timeperiod in instance.timegrouptimeperiod_set.all():
            timeperiod.ID_PD_TM.delete()
        TimeGroupTimePeriod.objects.filter(ID_GP_TM=instance.ID_GP_TM).delete()
        for time_period in time_period_data:
            time_period['LU_UOM_DRN'] = uom_instance
            time_period_instance = TimePeriod.objects.create(**time_period)
            timegroup_time_period = TimeGroupTimePeriod(
                ID_PD_TM=time_period_instance, ID_GP_TM=instance)
            timegroup_time_period.save()
        return instance

    class Meta:
        model = TimeGroup
        fields = ["ID_GP_TM", "NM_GP_TM", "DE_GP_TM", "uom", "time_period"]


class TimeGroupRetriveSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    uom = serializers.SerializerMethodField(read_only=True)
    time_period = serializers.SerializerMethodField(
        read_only=True)

    def get_time_period(self, obj):
        '''method to get assigned timeperiod'''
        tp_list = TimeGroupTimePeriodSerializer(
            obj.timegrouptimeperiod_set.all(), many=True).data
        return tp_list

    def get_uom(self, obj):
        '''get unit of measurement'''
        try:
            tg_tp = TimeGroupTimePeriod.objects.filter(
                ID_GP_TM=obj.ID_GP_TM).first().ID_PD_TM.LU_UOM_DRN
            uom = UomSerializerGet(tg_tp).data
        except TimeGroupTimePeriod.DoesNotExist:
            uom = ''
        return uom

    class Meta:
        model = TimeGroup
        fields = ["ID_GP_TM", "NM_GP_TM", "DE_GP_TM", "status", "createdby",
                  "createddate", "updatedby", "updateddate", "uom", "time_period"]


class TimeGroupListSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    uom = serializers.SerializerMethodField(read_only=True)
    weekdays = serializers.SerializerMethodField(
        read_only=True)

    def get_weekdays(self, obj):
        '''method to get assigned timeperiod'''
        wd_result = None
        wd_list = list(set(x['NM_PD_TM'] for x in TimeGroupTimePeriodSerializer(
            obj.timegrouptimeperiod_set.all(), many=True).data if x['status'] == 'A'))
        if len(wd_list) == 7:
            wd_result = "Daily"
        else:
            wd_result = ", ".join(wd_list)
        return wd_result

    def get_uom(self, obj):
        '''get unit of measurement'''
        try:
            tg_tp = TimeGroupTimePeriod.objects.filter(
                ID_GP_TM=obj.ID_GP_TM).first().ID_PD_TM.LU_UOM_DRN
            uom = UomSerializerGet(tg_tp).data['CD_UOM']
        except TimeGroupTimePeriod.DoesNotExist:
            uom = ''
        return uom

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
        model = TimeGroup
        fields = ["ID_GP_TM", "NM_GP_TM", "DE_GP_TM", "status", "createdby",
                  "createddate", "updatedby", "updateddate", "uom", "weekdays"]


class TimeGroupSerializer(serializers.ModelSerializer):
    '''TimeGroup serializer'''
    class Meta:
        model = TimeGroup
        fields = ["ID_GP_TM", "NM_GP_TM", "DE_GP_TM", "status"]
