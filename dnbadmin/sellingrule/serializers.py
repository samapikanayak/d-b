'''selling rule serializer'''
from rest_framework import serializers
from django.contrib.auth.models import User
from depositrule.models import DepositRule
from .models import ItemTenderRestrictionGroup, ItemSellingRule


class ItemTenderRestrictionGroupSerializer(serializers.ModelSerializer):
    '''
    ItemTenderRestrictionGroupSerializer
    '''
    class Meta:
        '''
        ItemTenderRestrictionGroupSerializer Meta class
        '''
        model = ItemTenderRestrictionGroup
        fields = "__all__"


class ItemSellingRuleSerializer(serializers.ModelSerializer):
    '''
    Item Selling Serializer
    '''

    class Meta:
        '''
        Itme Selling Rule Meta class
        '''
        model = ItemSellingRule
        fields = '__all__'


class SellingRulestatusSerializer(serializers.ModelSerializer):
    '''deposit rule status serializer'''

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    class Meta:
        model = ItemSellingRule
        fields = ["ID_RU_ITM_SL", "status"]
        read_only_fields = ["ID_RU_ITM_SL"]


class DepositRuleSerializer(serializers.ModelSerializer):
    '''DepositRule Serializer'''
    class Meta:
        model = DepositRule
        fields = '__all__'


class SellingRuleCreateSerializer(serializers.ModelSerializer):
    '''create update serializer'''
    NM_RU_ITM_SL = serializers.CharField(
        max_length=40, required=True, help_text="Title")
    DE_RU_ITM_SL = serializers.CharField(
        max_length=255, required=True, help_text="Description")

    def create(self, validated_data):
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        srule_instance = ItemSellingRule.objects.create(**validated_data)
        return srule_instance

    def update(self, instance, validated_data):
        request = self.context['request']
        current_user = request.user
        instance.NM_RU_ITM_SL = validated_data.get(
            'NM_RU_ITM_SL', instance.NM_RU_ITM_SL)
        instance.DE_RU_ITM_SL = validated_data.get(
            'DE_RU_ITM_SL', instance.DE_RU_ITM_SL)
        instance.status = validated_data.get('status', instance.status)
        instance.ID_RU_DS = validated_data.get('ID_RU_DS', instance.ID_RU_DS)
        instance.DC_ITM_SLS = validated_data.get(
            'DC_ITM_SLS', instance.DC_ITM_SLS)
        instance.expired_date = validated_data.get(
            'expired_date', instance.expired_date)
        instance.FL_CPN_RST = validated_data.get(
            'FL_CPN_RST', instance.FL_CPN_RST)
        instance.FL_CPN_ELTNC = validated_data.get(
            'FL_CPN_ELTNC', instance.FL_CPN_ELTNC)
        instance.FL_ENR_PRC_RQ = validated_data.get(
            'FL_ENR_PRC_RQ', instance.FL_ENR_PRC_RQ)
        instance.FL_ENT_WT_RQ = validated_data.get(
            'FL_ENT_WT_RQ', instance.FL_ENT_WT_RQ)
        instance.FL_DSC_EM_ALW = validated_data.get(
            'FL_DSC_EM_ALW', instance.FL_DSC_EM_ALW)
        instance.FL_CPN_ALW_MULTY = validated_data.get(
            'FL_CPN_ALW_MULTY', instance.FL_CPN_ALW_MULTY)
        instance.FL_KY_PRH_RPT = validated_data.get(
            'FL_KY_PRH_RPT', instance.FL_KY_PRH_RPT)
        instance.FL_PRC_VS_VR = validated_data.get(
            'FL_PRC_VS_VR', instance.FL_PRC_VS_VR)
        instance.FL_PNT_FQ_SHPR = validated_data.get(
            'FL_PNT_FQ_SHPR', instance.FL_PNT_FQ_SHPR)
        instance.QU_UN_BLK_MXM = validated_data.get(
            'QU_UN_BLK_MXM', instance.QU_UN_BLK_MXM)
        instance.QU_MNM_SLS_UN = validated_data.get(
            'QU_MNM_SLS_UN', instance.QU_MNM_SLS_UN)
        instance.updatedby = current_user.id
        instance.save()
        return instance

    class Meta:
        model = ItemSellingRule
        fields = ["ID_RU_ITM_SL", "NM_RU_ITM_SL", "DE_RU_ITM_SL", "status", "ID_RU_DS", "DC_ITM_SLS", "expired_date", "FL_CPN_RST", "FL_CPN_ELTNC",
                  "FL_ENR_PRC_RQ", "FL_ENT_WT_RQ", "FL_DSC_EM_ALW", "FL_CPN_ALW_MULTY", "FL_KY_PRH_RPT", "FL_PRC_VS_VR", "FL_PNT_FQ_SHPR", "QU_UN_BLK_MXM", "QU_MNM_SLS_UN"]


class SellingRuleRetriveSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    ID_RU_DS = serializers.SerializerMethodField(
        read_only=True)

    def get_ID_RU_DS(self, obj):
        '''method to get assigned deposit rule'''
        tp_list = DepositRuleSerializer(obj.ID_RU_DS).data
        return tp_list

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
        model = ItemSellingRule
        fields = ["ID_RU_ITM_SL", "NM_RU_ITM_SL", "DE_RU_ITM_SL", "status", "ID_RU_DS", "DC_ITM_SLS",
                  "expired_date", "FL_CPN_RST", "FL_CPN_ELTNC",
                  "FL_ENR_PRC_RQ", "FL_ENT_WT_RQ", "FL_DSC_EM_ALW", "FL_CPN_ALW_MULTY", "FL_KY_PRH_RPT",
                  "FL_PRC_VS_VR", "FL_PNT_FQ_SHPR", "QU_UN_BLK_MXM", "QU_MNM_SLS_UN", "createdby", "createddate",
                  "updatedby", "updateddate", ]


class SellingRuleListSerializer(serializers.ModelSerializer):
    '''Retrive serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    deposit_rule = serializers.SerializerMethodField(
        read_only=True)

    def get_deposit_rule(self, obj):
        '''method to get assigned deposit rule'''
        dp_rule = DepositRuleSerializer(obj.ID_RU_DS).data['LU_UOM_DS_PD']
        return dp_rule

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
        model = ItemSellingRule
        fields = ["ID_RU_ITM_SL", "NM_RU_ITM_SL", "DE_RU_ITM_SL", "status", "DC_ITM_SLS",
                  "expired_date", "FL_CPN_RST", "FL_CPN_ELTNC",
                  "FL_ENR_PRC_RQ", "FL_ENT_WT_RQ", "FL_DSC_EM_ALW", "FL_CPN_ALW_MULTY", "FL_KY_PRH_RPT",
                  "FL_PRC_VS_VR", "FL_PNT_FQ_SHPR", "QU_UN_BLK_MXM", "QU_MNM_SLS_UN", "createdby", "createddate",
                  "updatedby", "updateddate", "deposit_rule"]
