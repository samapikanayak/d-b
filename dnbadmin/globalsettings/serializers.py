'''global setting serializer'''
import logging
from pickle import TRUE
from typing import Any
from django.contrib.auth.models import User
from rest_framework import serializers
from globalsettings.models import GlobalSetting, BusinessUnitSetting
from store.models import BusinessUnit

logger = logging.getLogger(__name__)


class BusinessUnitSettingListSerializer(serializers.ModelSerializer):
    '''business unit and setting map'''
    b_unit_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BusinessUnitSetting
        fields = ['ID_BSN_UN', 'b_unit_name']

    def get_b_unit_name(self, obj):
        '''return business unit name'''
        return obj.ID_BSN_UN.NM_BSN_UN


class GlobalSettingSerializer(serializers.ModelSerializer):
    '''global setting create serializer'''
    b_unit = serializers.CharField(
        write_only=True, max_length=200, required=TRUE, help_text="Selected Business Unit Ids, comma seperated")

    def create(self, validated_data):
        b_unit_data = validated_data.pop('b_unit', None)
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        globalsetting = GlobalSetting.objects.create(**validated_data)
        b_unit_data = list(b_unit_data.split(","))
        for each_b_unit in b_unit_data:
            b_unit_obj = BusinessUnit.objects.filter(
                ID_BSN_UN=int(each_b_unit)).first()
            if b_unit_obj:
                unit_setting = BusinessUnitSetting(
                    ID_BSN_UN=b_unit_obj, ID_GB_STNG=globalsetting)
                unit_setting.save()
        logger.info('Global setting create serializer')
        return globalsetting

    class Meta:
        model = GlobalSetting
        fields = ["ID_GB_STNG", "name", "status", "page_title", "page_description", "page_keyword", "meta_locale", "meta_robots", "meta_referral", "meta_rights", "og_type",
                  "og_url", "og_title", "og_description", "og_image", "og_locale", "twitter_card",
                  "view_point", "script", "ID_LGE", "ID_BA_DFMT", "ID_BA_TZN", "b_unit"]


class GlobalSettingListSerializer(serializers.ModelSerializer):
    '''global setting list serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    b_unit = serializers.CharField(
        write_only=True, max_length=200, required=TRUE, help_text="Selected Business Unit Ids, comma seperated")
    b_unit_assigned = serializers.SerializerMethodField(
        read_only=True)

    def get_b_unit_assigned(self, obj):
        '''method to represent connected bunit to comma seperated string'''
        bunit_list = ", ".join(
            [x['b_unit_name'] for x in BusinessUnitSettingListSerializer(
                obj.businessunitsetting_set.all(), many=True).data])
        return bunit_list

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
        model = GlobalSetting
        fields = ["ID_GB_STNG", "name", "status", "page_title", "page_description", "page_keyword", "meta_locale", "meta_robots", "meta_referral", "meta_rights", "og_type",
                  "og_url", "og_title", "og_description", "og_image", "og_locale", "twitter_card",
                  "view_point", "script", "ID_LGE", "ID_BA_DFMT", "ID_BA_TZN", "b_unit", "createdby", "createddate", "updatedby", "updateddate", "b_unit_assigned"]


class GlobalSettingRetrieveSerializer(serializers.ModelSerializer):
    '''global setting list serializer'''
    b_unit = serializers.CharField(
        write_only=True, max_length=200, required=TRUE, help_text="Selected Business Unit Ids, comma seperated")
    b_unit_assigned = serializers.SerializerMethodField(
        read_only=True)

    def get_b_unit_assigned(self, obj):
        '''method to get assigned business units'''
        bunit_list = BusinessUnitSettingListSerializer(
            obj.businessunitsetting_set.all(), many=True).data
        return bunit_list

    class Meta:
        model = GlobalSetting
        fields = ["ID_GB_STNG", "name", "status", "page_title", "page_description", "page_keyword", "meta_locale", "meta_robots", "meta_referral", "meta_rights", "og_type",
                  "og_url", "og_title", "og_description", "og_image", "og_locale", "twitter_card",
                  "view_point", "script", "ID_LGE", "ID_BA_DFMT", "ID_BA_TZN", "b_unit", "createdby", "createddate", "updatedby", "updateddate", "b_unit_assigned"]
        depth = 1


class GlobalSettingUpdateSerializer(serializers.ModelSerializer):
    '''global setting fetch update serializer'''

    def update(self, instance, validated_data):
        b_unit_data = validated_data.pop('b_unit', None)
        request = self.context['request']
        current_user = request.user
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.page_title = validated_data.get(
            'page_title', instance.page_title)
        instance.page_description = validated_data.get(
            'page_description', instance.page_description)
        instance.page_keyword = validated_data.get(
            'page_keyword', instance.page_keyword)
        instance.meta_locale = validated_data.get(
            'meta_locale', instance.meta_locale)
        instance.meta_robots = validated_data.get(
            'meta_robots', instance.meta_robots)
        instance.meta_referral = validated_data.get(
            'meta_referral', instance.meta_referral)
        instance.meta_rights = validated_data.get(
            'meta_rights', instance.meta_rights)
        instance.og_type = validated_data.get('og_type', instance.og_type)
        instance.og_url = validated_data.get('og_url', instance.og_url)
        instance.og_title = validated_data.get('og_title', instance.og_title)
        instance.og_description = validated_data.get(
            'og_description', instance.og_description)
        instance.og_image = validated_data.get('og_image', instance.og_image)
        instance.og_locale = validated_data.get(
            'og_locale', instance.og_locale)
        instance.twitter_card = validated_data.get(
            'twitter_card', instance.twitter_card)
        instance.view_point = validated_data.get(
            'view_point', instance.view_point)
        instance.script = validated_data.get('script', instance.script)
        instance.ID_LGE = validated_data.get('ID_LGE', instance.ID_LGE)
        instance.ID_BA_DFMT = validated_data.get(
            'ID_BA_DFMT', instance.ID_BA_DFMT)
        instance.ID_BA_TZN = validated_data.get(
            'ID_BA_TZN', instance.ID_BA_TZN)
        instance.updatedby = current_user.id
        instance.save()
        b_unit_data = list(b_unit_data.split(","))
        BusinessUnitSetting.objects.filter(
            ID_GB_STNG=instance.ID_GB_STNG).delete()
        for each_b_unit in b_unit_data:
            b_unit_obj = BusinessUnit.objects.get(pk=each_b_unit)
            if b_unit_obj:
                unit_setting = BusinessUnitSetting(
                    ID_BSN_UN=b_unit_obj, ID_GB_STNG=instance)
                unit_setting.save()
        logger.info('Global setting update serializer')
        return instance
    b_unit_added = serializers.SerializerMethodField(
        read_only=True, help_text="Selected Business Unit Ids, comma seperated")
    b_unit = serializers.CharField(
        write_only=True, max_length=200, required=TRUE, help_text="Selected Business Unit Ids, comma seperated")

    def get_b_unit_added(self, obj):
        '''method to represent connected bunit to comma seperated string'''
        bunit_list = ", ".join(
            [f"{x.ID_BSN_UN.ID_BSN_UN}" for x in BusinessUnitSetting.objects.filter(
                ID_GB_STNG=obj.ID_GB_STNG).all()])
        return bunit_list

    class Meta:
        model = GlobalSetting
        fields = ["ID_GB_STNG", "name", "status", "page_title", "page_description", "page_keyword", "meta_locale", "meta_robots", "meta_referral", "meta_rights", "og_type",
                  "og_url", "og_title", "og_description", "og_image", "og_locale", "twitter_card", "view_point", "script", "ID_LGE", "ID_BA_DFMT", "ID_BA_TZN", "b_unit_added", "b_unit"]


class GlobalSettingstatusSerializer(serializers.ModelSerializer):
    '''global setting status serializer'''

    def update(self, instance, validated_data):
        request = self.context['request']
        current_user = request.user
        instance.status = validated_data.get('status', instance.status)
        instance.updatedby = current_user.id
        instance.save()
        logger.info('Global setting stat update serializer')
        return instance

    class Meta:
        model = GlobalSetting
        fields = ["ID_GB_STNG", "name", "status"]
        read_only_fields = ["ID_GB_STNG", "name"]


class ChangePasswordSerializer(serializers.Serializer):
    '''
    change password serializer
    '''
    new_password = serializers.CharField(max_length=20, min_length=8)
    retype_password = serializers.CharField(max_length=20)

    def create(self, validated_data) -> Any:
        return super().create(validated_data)

    def validate(self, data):
        if not data["new_password"] == data["retype_password"]:
            raise serializers.ValidationError("password does not match")
        return data
