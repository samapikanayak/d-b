'''pos serializer'''
import logging
from pickle import TRUE
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from pos_department.models import POSDepartment, BusinessUnitGroupPOSDepartment, BusinessUnitGroup, ItemSellingRule

logger = logging.getLogger(__name__)


class POSDepartmentCreateSerializer(serializers.ModelSerializer):
    '''create update serializer'''
    ID_BSNGP = serializers.IntegerField(
        write_only=True, required=TRUE, help_text="Business Unit Group ID")

    def validate_ID_DPT_PS_PRNT(self, value):
        """
        Check that ID_DPT_PS_PRNT is not same as pos id
        """
        if self.instance and value and value.ID_DPT_PS == self.instance.ID_DPT_PS:
            raise serializers.ValidationError(
                "Wrong parent POS Department selected")
        return value

    def create(self, validated_data):
        bsngp_data = validated_data.pop('ID_BSNGP')
        bsngp_instance = get_object_or_404(
            BusinessUnitGroup, ID_BSNGP=bsngp_data)
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        pos_instance = POSDepartment.objects.create(**validated_data)
        pos_bsngp = BusinessUnitGroupPOSDepartment(
            ID_BSNGP=bsngp_instance, ID_DPT_PS=pos_instance)
        pos_bsngp.save()
        return pos_instance

    def update(self, instance, validated_data):
        bsngp_data = validated_data.pop('ID_BSNGP')
        bsngp_instance = get_object_or_404(
            BusinessUnitGroup, ID_BSNGP=bsngp_data)
        request = self.context['request']
        current_user = request.user
        instance.NM_DPT_PS = validated_data.get(
            'NM_DPT_PS', instance.NM_DPT_PS)
        instance.status = validated_data.get('status', instance.status)
        instance.ID_DPT_PS_PRNT = validated_data.get(
            'ID_DPT_PS_PRNT', instance.ID_DPT_PS_PRNT)
        instance.ID_RU_ITM_SL = validated_data.get(
            'ID_RU_ITM_SL', instance.ID_RU_ITM_SL)
        instance.updatedby = current_user.id
        instance.save()
        BusinessUnitGroupPOSDepartment.objects.filter(
            ID_DPT_PS=instance.ID_DPT_PS).delete()
        pos_bsngp = BusinessUnitGroupPOSDepartment(
            ID_BSNGP=bsngp_instance, ID_DPT_PS=instance)
        pos_bsngp.save()
        return instance

    class Meta:
        model = POSDepartment
        fields = ["ID_DPT_PS", "NM_DPT_PS", "status",
                  "ID_DPT_PS_PRNT", "ID_RU_ITM_SL", "ID_BSNGP"]


class ItemSellingRuleSerializer(serializers.ModelSerializer):
    '''ItemSellingRule Serializer'''
    class Meta:
        model = ItemSellingRule
        fields = ["ID_RU_ITM_SL", "NM_RU_ITM_SL"]


class BusinessUnitGroupPOSDepartmentSerializer(serializers.ModelSerializer):
    '''pos association with business unit group serializer'''
    NM_BSNGP = serializers.SerializerMethodField(read_only=True)

    def get_NM_BSNGP(self, obj):
        '''get business group name'''
        if obj.ID_BSNGP:
            return obj.ID_BSNGP.NM_BSNGP

    class Meta:
        model = BusinessUnitGroupPOSDepartment
        fields = ["ID_BSNGP", "NM_BSNGP"]


class POSDepartmentListSerializer(serializers.ModelSerializer):
    '''Pos List Serializer'''
    pos_code = serializers.SerializerMethodField(read_only=True)

    def get_pos_code(self, obj):
        '''generate pos code'''
        return 'PO'+str(10000+obj.ID_DPT_PS)

    class Meta:
        model = POSDepartment
        fields = ["ID_DPT_PS", "pos_code", "NM_DPT_PS", "status"]


class POSDepartmentRetriveSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    item_selling_rule = serializers.SerializerMethodField(read_only=True)
    b_unit_group = BusinessUnitGroupPOSDepartmentSerializer(
        source='businessunitgroupposdepartment_set', many=True)
    pos_code = serializers.SerializerMethodField(read_only=True)
    ID_DPT_PS_PRNT = serializers.SerializerMethodField(read_only=True)

    def get_item_selling_rule(self, obj):
        '''get selling rule details'''
        if obj.ID_RU_ITM_SL:
            data = ItemSellingRuleSerializer(obj.ID_RU_ITM_SL).data
        else:
            data = ''
        return data

    def get_pos_code(self, obj):
        '''generate pos code'''
        return 'PO'+str(10000+obj.ID_DPT_PS)

    def get_ID_DPT_PS_PRNT(self, obj):
        '''get parent pos details'''
        if obj.ID_DPT_PS_PRNT:
            data = POSDepartmentListSerializer(obj.ID_DPT_PS_PRNT).data
        else:
            data = ''
        return data

    class Meta:
        model = POSDepartment
        fields = ["ID_DPT_PS", "pos_code", "NM_DPT_PS", "status",
                  "ID_DPT_PS_PRNT", "item_selling_rule", "b_unit_group", "createdby",
                  "createddate", "updatedby", "updateddate", ]


class POSDepartmentSerializer(serializers.ModelSerializer):
    '''List serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    item_selling_rule = serializers.SerializerMethodField(read_only=True)
    b_unit_group = serializers.SerializerMethodField(read_only=True)
    pos_code = serializers.SerializerMethodField(read_only=True)
    ID_DPT_PS_PRNT = serializers.SerializerMethodField(read_only=True)

    def get_b_unit_group(self, obj):
        ''' Business Unit Group '''
        bunit_list = BusinessUnitGroupPOSDepartmentSerializer(
            obj.businessunitgroupposdepartment_set.all(), many=True).data[0]['NM_BSNGP']
        return bunit_list

    def get_item_selling_rule(self, obj):
        '''get selling rule details'''
        if obj.ID_RU_ITM_SL:
            data = ItemSellingRuleSerializer(
                obj.ID_RU_ITM_SL).data['NM_RU_ITM_SL']
        else:
            data = ''
        return data

    def get_pos_code(self, obj):
        '''generate pos code'''
        return 'PO'+str(10000+obj.ID_DPT_PS)

    def get_ID_DPT_PS_PRNT(self, obj):
        '''get parent pos details'''
        if obj.ID_DPT_PS_PRNT:
            data = POSDepartmentListSerializer(
                obj.ID_DPT_PS_PRNT).data['pos_code']
        else:
            data = ''
        return data

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
        model = POSDepartment
        fields = ["ID_DPT_PS", "pos_code", "NM_DPT_PS", "status",
                  "ID_DPT_PS_PRNT", "item_selling_rule", "b_unit_group", "createdby",
                  "createddate", "updatedby", "updateddate", ]
