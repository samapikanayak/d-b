''' Accesscontrol Serializer File '''
import resource
from rest_framework import serializers
from .models import Resource, WorkGroup, GroupResourceAccess, StoreWorkGroup


class ResourceSerializer(serializers.ModelSerializer):
    ''' Resource Serializer Class '''
    class Meta:
        model = Resource
        fields = '__all__'


class WorkGroupSerializer(serializers.ModelSerializer):
    ''' WorkGroup Serializer '''
    business_units = serializers.SerializerMethodField(
        read_only=True)

    def get_business_units(self, obj):
        '''method to represent connected bunit to comma seperated string'''
        bunit_list = ", ".join(
            [x['b_unit_name'] for x in StoreWorkGroupSerializer(
                obj.storeworkgroup_set.all(), many=True).data])
        return bunit_list

    class Meta:
        model = WorkGroup
        fields = "__all__"


class GroupResourceAccessSerializer(serializers.ModelSerializer):
    ''' Group Resource Access Serializer '''
    DE_RS = serializers.SerializerMethodField(read_only=True)

    def get_DE_RS(self, obj):
        '''return resource name'''
        return obj.ID_RS.DE_RS

    class Meta:
        model = GroupResourceAccess
        fields = ['ID_RS', 'FL_ACS_GP_RD', 'FL_ACS_GP_WR', 'DE_RS']


class StoreWorkGroupSerializer(serializers.ModelSerializer):
    ''' Group Resource Access Serializer '''
    b_unit_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StoreWorkGroup
        fields = ['ID_BSN_UN', 'storeworkgroup_id', 'b_unit_name']

    def get_b_unit_name(self, obj):
        '''return business unit name'''
        return obj.ID_BSN_UN.NM_BSN_UN


class WorkGroupCreateSerializer(serializers.ModelSerializer):
    ''' WorkGroup Create Serializer '''
    resources = GroupResourceAccessSerializer(
        many=True, write_only=True, allow_null=True, required=False,)
    business_unit = StoreWorkGroupSerializer(
        many=True, write_only=True, allow_null=True, required=False,)

    class Meta:
        model = WorkGroup
        fields = "__all__"
        extra_kwargs = {
            "createddate": {
                "read_only": True
            },
            "createdby": {
                "read_only": True
            },
            "updateddate": {
                "read_only": True
            },
            "updatedby": {
                "read_only": True
            }
        }

    def create(self, validated_data):
        resource_data = validated_data.pop('resources')
        business_unit_data = validated_data.pop('business_unit')
        workgroup_instance = WorkGroup.objects.create(**validated_data)
        print(f"Workgroup Instance : {workgroup_instance}")
        for resource in resource_data:
            resource['ID_GP_WRK'] = workgroup_instance
            GroupResourceAccess.objects.create(**resource)
        for business in business_unit_data:
            business['ID_GP_WRK'] = workgroup_instance
            StoreWorkGroup.objects.create(**business)

        return workgroup_instance


class WorkGroupUpdateSerializer(serializers.ModelSerializer):
    '''update serializer'''
    business_unit = StoreWorkGroupSerializer(
        many=True, write_only=True, required=True, help_text="Selected Business Unit Ids")
    resources = GroupResourceAccessSerializer(
        many=True, write_only=True, allow_null=True, required=False,  help_text="Resource Access set")

    def update(self, instance, validated_data):
        b_unit_data = validated_data.pop('business_unit')
        resource_data = validated_data.pop('resources')
        request = self.context['request']
        current_user = request.user

        instance.ID_GP_WRK_PRNT = validated_data.get(
            'ID_GP_WRK_PRNT', instance.ID_GP_WRK_PRNT)
        instance.DE_GP_WRK = validated_data.get(
            'DE_GP_WRK', instance.DE_GP_WRK)
        instance.NM_GP_WRK = validated_data.get(
            'NM_GP_WRK', instance.NM_GP_WRK)
        instance.access_type = validated_data.get(
            'access_type', instance.access_type)
        instance.welcome_screen = validated_data.get(
            'welcome_screen', instance.welcome_screen)
        instance.updatedby = current_user.id
        instance.save()

        StoreWorkGroup.objects.filter(
            ID_GP_WRK=instance.ID_GP_WRK).delete()
        GroupResourceAccess.objects.filter(
            ID_GP_WRK=instance.ID_GP_WRK).delete()

        # operator_instance = instance

        for b_unit in b_unit_data:
            b_unit['ID_GP_WRK'] = instance
            StoreWorkGroup.objects.create(
                **b_unit)

        for resource in resource_data:
            resource['ID_GP_WRK'] = instance
            GroupResourceAccess.objects.create(**resource)

        return instance

    class Meta:
        model = WorkGroup
        fields = ["ID_GP_WRK", "ID_GP_WRK_PRNT", "DE_GP_WRK", "NM_GP_WRK",
                  "status", "access_type", "welcome_screen", "business_unit", "resources"]


class WorkGroupRetriveSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    business_units = StoreWorkGroupSerializer(
        source='storeworkgroup_set', many=True)
    resources = GroupResourceAccessSerializer(
        source='groupresourceaccess_set', many=True)

    class Meta:
        model = WorkGroup
        fields = ["ID_GP_WRK", "ID_GP_WRK_PRNT", "DE_GP_WRK", "NM_GP_WRK",
                  "status", "business_units", "access_type", "resources", "welcome_screen", "createdby",
                  "createddate", "updatedby", "updateddate"]
