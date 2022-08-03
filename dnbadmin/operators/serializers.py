'''pos serializer'''
import logging
from pickle import TRUE

from accesscontrol.models import (AccessPassword, Operator,
                                  OperatorBusinessUnitAssignment,
                                  OperatorGroup, OperatorResourceAccess,
                                  Resource, WorkGroup)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers

logger = logging.getLogger(__name__)


class OperatorBusinessUnitAssignmentSerializer(serializers.ModelSerializer):
    '''OperatorBusinessUnitAssignment Serializer'''
    b_unit_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OperatorBusinessUnitAssignment
        fields = ['ID_ASGMT_OPR_LCN', 'ID_BSN_UN', 'b_unit_name']

    def get_b_unit_name(self, obj):
        '''return business unit name'''
        return obj.ID_BSN_UN.NM_BSN_UN


class OperatorResourceAccessSerializer(serializers.ModelSerializer):
    '''OperatorResourceAccess Serializer'''
    resource_details = serializers.SerializerMethodField(read_only=True)

    def get_resource_details(self, obj):
        '''method to get resource_details'''
        tp_list = ResourceSerializer(
            obj.ID_RS).data
        return tp_list

    class Meta:
        model = OperatorResourceAccess
        fields = ["ID_ACS_OPR_RS", "ID_RS",
                  "PS_ACS_RD", "PR_ACS_WR", "resource_details"]
        extra_kwargs = {
            "ID_ACS_OPR_RS": {
                "read_only": True
            }
        }


class OperatorCreateSerializer(serializers.ModelSerializer):
    '''create serializer'''
    EMAIL_USR = serializers.EmailField(
        required=TRUE, max_length=254, min_length=6, help_text="Email Address")
    PW_ACS_OPR = serializers.CharField(
        help_text="AccessPassword", max_length=20, min_length=6)
    NM_USR = serializers.CharField(
        help_text="UserName", max_length=40, min_length=5)
    b_unit = OperatorBusinessUnitAssignmentSerializer(
        many=True, write_only=True, required=TRUE, help_text="Selected Business Unit Ids")
    permission_set = serializers.CharField(
        write_only=True, allow_null=True, required=False, allow_blank=True, help_text="Selected permission set")
    resources = OperatorResourceAccessSerializer(
        many=True, write_only=True, allow_null=True, required=False,  help_text="Resource Access set")

    def create(self, validated_data):
        b_unit_data = validated_data.pop('b_unit')
        permission_set_data = validated_data.pop('permission_set')
        if validated_data['RS_TYP_OPR'] == 'GA' and permission_set_data:
            wrkgp_instance = get_object_or_404(
                WorkGroup, ID_GP_WRK=permission_set_data)
        resources_data = validated_data.pop('resources')
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        operator_instance = Operator.objects.create(**validated_data)
        access_password = AccessPassword(
            ID_OPR=operator_instance, PS_ACS_OPR=validated_data['PW_ACS_OPR'])
        access_password.save()
        for b_unit in b_unit_data:
            b_unit['ID_OPR'] = operator_instance
            b_unit['NU_OPR'] = 10000+operator_instance.ID_OPR
            OperatorBusinessUnitAssignment.objects.create(
                **b_unit)
        if validated_data['RS_TYP_OPR'] == 'RA':
            for resources in resources_data:
                resources['ID_OPR'] = operator_instance
                OperatorResourceAccess.objects.create(
                    **resources)
        elif validated_data['RS_TYP_OPR'] == 'GA' and permission_set_data:
            op_grp = OperatorGroup(
                ID_OPR=operator_instance, ID_GP_WRK=wrkgp_instance)
            op_grp.save()
        return operator_instance

    class Meta:
        model = Operator
        fields = ["ID_OPR", "ACCS_TYP_OPR", "NM_USR", "EMAIL_USR",
                  "PW_ACS_OPR", "RS_TYP_OPR", "b_unit", "permission_set", "resources"]


class OperatorUpdateSerializer(serializers.ModelSerializer):
    '''update serializer'''
    EMAIL_USR = serializers.EmailField(
        required=TRUE, max_length=254, min_length=6, help_text="Email Address")
    PW_ACS_OPR = serializers.CharField(
        help_text="AccessPassword", allow_null=True, required=False, allow_blank=True, max_length=20, min_length=6)
    NM_USR = serializers.CharField(
        help_text="UserName", max_length=40, min_length=5)
    b_unit = OperatorBusinessUnitAssignmentSerializer(
        many=True, write_only=True, required=TRUE, help_text="Selected Business Unit Ids")
    permission_set = serializers.CharField(
        write_only=True, allow_null=True, required=False, allow_blank=True, help_text="Selected permission set")
    resources = OperatorResourceAccessSerializer(
        many=True, write_only=True, allow_null=True, required=False,  help_text="Resource Access set")

    def update(self, instance, validated_data):
        b_unit_data = validated_data.pop('b_unit')
        permission_set_data = validated_data.pop('permission_set')
        if validated_data['RS_TYP_OPR'] == 'GA' and permission_set_data:
            wrkgp_instance = get_object_or_404(
                WorkGroup, ID_GP_WRK=permission_set_data)
        resources_data = validated_data.pop('resources')
        request = self.context['request']
        current_user = request.user
        instance.ACCS_TYP_OPR = validated_data.get(
            'ACCS_TYP_OPR', instance.ACCS_TYP_OPR)
        instance.NM_USR = validated_data.get('NM_USR', instance.NM_USR)
        instance.EMAIL_USR = validated_data.get(
            'EMAIL_USR', instance.EMAIL_USR)
        if validated_data['PW_ACS_OPR']:
            instance.PW_ACS_OPR = validated_data.get(
                'PW_ACS_OPR', instance.PW_ACS_OPR)
        instance.RS_TYP_OPR = validated_data.get(
            'RS_TYP_OPR', instance.RS_TYP_OPR)
        instance.updatedby = current_user.id
        instance.save()
        AccessPassword.objects.filter(ID_OPR=instance.ID_OPR).delete()
        OperatorBusinessUnitAssignment.objects.filter(
            ID_OPR=instance.ID_OPR).delete()
        OperatorResourceAccess.objects.filter(ID_OPR=instance.ID_OPR).delete()
        OperatorGroup.objects.filter(ID_OPR=instance.ID_OPR).delete()
        operator_instance = instance
        access_password = AccessPassword(
            ID_OPR=operator_instance, PS_ACS_OPR=validated_data['PW_ACS_OPR'])
        access_password.save()
        for b_unit in b_unit_data:
            b_unit['ID_OPR'] = operator_instance
            b_unit['NU_OPR'] = 10000+operator_instance.ID_OPR
            OperatorBusinessUnitAssignment.objects.create(
                **b_unit)
        if validated_data['RS_TYP_OPR'] == 'RA':
            for resources in resources_data:
                resources['ID_OPR'] = operator_instance
                OperatorResourceAccess.objects.create(
                    **resources)
        elif validated_data['RS_TYP_OPR'] == 'GA' and permission_set_data:
            op_grp = OperatorGroup(
                ID_OPR=operator_instance, ID_GP_WRK=wrkgp_instance)
            op_grp.save()
        return operator_instance

    class Meta:
        model = Operator
        fields = ["ID_OPR", "ACCS_TYP_OPR", "NM_USR", "EMAIL_USR",
                  "PW_ACS_OPR", "RS_TYP_OPR", "b_unit", "permission_set", "resources"]
        extra_kwargs = {
            "PW_ACS_OPR": {"required": False}
        }


class OperatorListSerializer(serializers.ModelSerializer):
    '''Operator Serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    opr_code = serializers.SerializerMethodField(read_only=True)
    b_unit_assigned = serializers.SerializerMethodField(
        read_only=True)
    RS_TYP_OPR = serializers.SerializerMethodField(read_only=True)

    def get_b_unit_assigned(self, obj):
        '''method to represent connected bunit to comma seperated string'''
        bunit_list = ", ".join(
            [x['b_unit_name'] for x in OperatorBusinessUnitAssignmentSerializer(
                obj.operatorbusinessunitassignment_set.all(), many=True).data])
        return bunit_list

    def get_opr_code(self, obj):
        '''generate opr code'''
        return 'OPR'+str(10000+obj.ID_OPR)

    def get_RS_TYP_OPR(self, obj):
        '''generate opr code'''
        return obj.get_RS_TYP_OPR_display()

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
        model = Operator
        fields = ["ID_OPR", "status", "opr_code", "NM_USR", "EMAIL_USR", "b_unit_assigned",
                  "RS_TYP_OPR", "createdby", "createddate", "updatedby", "updateddate"]


class OperatorGroupSerializer(serializers.ModelSerializer):
    '''OperatorGroup Serializer'''
    permission_set_name = serializers.SerializerMethodField(read_only=True)

    def get_permission_set_name(self, obj):
        '''return permission set name'''
        return obj.ID_GP_WRK.DE_GP_WRK

    class Meta:
        model = OperatorGroup
        fields = ["ID_GP_OPR", "ID_GP_WRK", "permission_set_name"]
        extra_kwargs = {
            "ID_GP_OPR": {
                "read_only": True
            }
        }


class OperatorRetriveSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    b_unit = OperatorBusinessUnitAssignmentSerializer(
        source='operatorbusinessunitassignment_set', many=True)
    resources = OperatorResourceAccessSerializer(
        source='operatorresourceaccess_set', many=True)
    permission_set = OperatorGroupSerializer(
        source='operatorgroup_set', many=True)

    class Meta:
        model = Operator
        fields = ["ID_OPR", "ACCS_TYP_OPR", "NM_USR", "EMAIL_USR",
                  "PW_ACS_OPR", "b_unit", "RS_TYP_OPR", "resources", "permission_set", "createdby",
                  "createddate", "updatedby", "updateddate"]


class ResourceSerializer(serializers.ModelSerializer):
    '''Resource Serializer'''
    class Meta:
        model = Resource
        fields = ["ID_RS", "DE_RS"]
