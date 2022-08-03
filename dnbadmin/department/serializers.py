'''Department Serializer'''
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    '''Serializer class of Department '''
    created_by = serializers.SerializerMethodField("get_created_by", read_only=True)
    updatedby = serializers.SerializerMethodField("get_updated_by", read_only=True)
    class Meta:
        '''Meta class for DepartmentSerializer'''
        model = Department
        fields = [
            "department_id","name", "business_unit_group_code", "description", "status", "createdby", "created_by", "createddate", "updatedby", "updateddate", "parent_department_id"
        ]
        extra_kwargs = {
            "parent_department_id": {"required": False},
            "createdby": {"write_only": True},
            "updatedby": {"write_only": True},
            "department_id": {"read_only": True},
        }

    def create(self, validated_data):
        '''custom create method for department'''
        request = self.context["request"]
        current_user = request.user
        validated_data["createdby"] = current_user.id
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''custom update method for department'''
        request = self.context["request"]
        current_user = request.user
        instance.updatedby = current_user.id
        instance.status = validated_data.get('status', instance.status)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.parent_department_id = validated_data.get('parent_department_id', instance.parent_department_id)
        instance.business_unit_group_code = validated_data.get('business_unit_group_code', instance.business_unit_group_code)
        instance.save()
        return instance

    def get_created_by(self, obj):
        '''return username'''
        if obj.createdby:
            try:
                user = User.objects.get(id=obj.createdby)
                user = user.username
            except User.DoesNotExist:
                user = "Annonymous"
            return user

    def get_updated_by(self, obj):
        '''return username'''
        if obj.updatedby:
            try:
                user = User.objects.get(id=obj.updatedby)
                user = user.username
            except User.DoesNotExist:
                user = "Annonymous"
            return user


class DepartmentstatusSerializer(serializers.ModelSerializer):
    '''department status serializer'''

    def update(self, instance, validated_data):
        request = self.context['request']
        current_user = request.user
        instance.status = validated_data.get('status', instance.status)
        instance.updatedby = current_user.id
        instance.save()
        return instance

    class Meta:
        '''DepartmentSerializer Meta class'''
        model = Department
        fields = ["department_id", "name", "status"]
        read_only_fields = ["department_id", "name"]
    