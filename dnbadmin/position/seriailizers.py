'''position serializer'''
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Position

class PositionSerializer(serializers.ModelSerializer):
    '''Serializer class of Position '''
    created_by = serializers.SerializerMethodField("get_created_by", read_only=True)
    updated_by = serializers.SerializerMethodField("get_updated_by", read_only=True)
    department_name = serializers.SerializerMethodField("get_dept_name", read_only=True)
    class Meta:
        '''Meta class for PositionSerializer'''
        model = Position
        fields = [
            "ID_PST","ID_LCN", "ID_JOB", "department_id", "NM_TTL", "DE_PST", "created_by", "updated_by", "status", "start_date", "end_date", "department_name"
        ]
        extra_kwargs = {
            "ID_PST": {"read_only": "True","required": False},
            "department_id": {"write_only": "True","required": False},
        }

    def create(self, validated_data):
        '''custom create method for position'''
        request = self.context["request"]
        current_user = request.user
        validated_data["createdby"] = current_user.id
        return Position.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''custom update method for position'''
        request = self.context["request"]
        current_user = request.user
        instance.updatedby = current_user.id
        instance.status = validated_data.get('status', instance.status)
        instance.NM_TTL = validated_data.get('NM_TTL', instance.NM_TTL)
        instance.DE_PST = validated_data.get('DE_PST', instance.DE_PST)
        instance.department_id = validated_data.get('department_id', instance.department_id)
        instance.ID_JOB = validated_data.get('ID_JOB', instance.ID_JOB)
        instance.ID_LCN = validated_data.get('ID_LCN', instance.ID_LCN)
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

    def get_dept_name(self, obj):
        '''return department name'''
        if obj.department_id:
            return obj.department_id.name


class PositionstatusSerializer(serializers.ModelSerializer):
    '''position status serializer'''

    def update(self, instance, validated_data):
        request = self.context['request']
        current_user = request.user
        instance.status = validated_data.get('status', instance.status)
        instance.updatedby = current_user.id
        instance.save()
        return instance

    class Meta:
        '''Position Meta class'''
        model = Position
        fields = ["ID_PST", "NM_TTL", "status"]
        read_only_fields = ["ID_PST", "NM_TTL"]
    