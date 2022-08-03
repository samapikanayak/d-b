from email.policy import default
from rest_framework import serializers
from .models import DepositRule
from globalsettings.utility import convert_datetime_timezone

class DepositRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositRule
        fields = "__all__"
        extra_kwargs = {
            "DATE_OF_CREATION":{"read_only": True, "required": False}
        }

class DepositRulestatusSerializer(serializers.ModelSerializer):
    '''deposit rule status serializer'''

    def update(self, instance, validated_data):
        instance.SC_RU_DS = validated_data.get('status', instance.status)
        instance.save()
        return instance

    class Meta:
        model = DepositRule
        fields = ["ID_RU_DS", "MO_DS", "SC_RU_DS"]
        read_only_fields = ["ID_RU_DS", "MO_DS"]


