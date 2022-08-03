'''taxonomy serializer'''
import logging
from rest_framework import serializers
from django.contrib.auth.models import User
from taxonomy.models import MerchandiseTemplateType, MerchandiseTemplate, MerchandiseTemplateControls, MerchandiseTemplateControlValue
from basics.models import CustomFormFieldType, CustomFormField, CustomFormFieldValue

logger = logging.getLogger(__name__)


class MerchandiseTemplateControlValueSerializer(serializers.ModelSerializer):
    '''MerchandiseTemplateControlValue Serializer'''
    customformfield_value = serializers.SerializerMethodField(read_only=True)

    def get_customformfield_value(self, obj):
        '''method to get customform field value'''
        tp_list = CustomFormFieldValueListSerializer(
            obj.ID_BA_CFF_VAL).data
        return tp_list

    class Meta:
        model = MerchandiseTemplateControlValue
        fields = ["ID_MRHRC_TMP_CNT_VL", "ID_MRHRC_TMP_CNT",
                  "ID_BA_CFF_VAL", "merchandisetemplatecontrol_value", "isdefault", "customformfield_value"]
        extra_kwargs = {
            "ID_MRHRC_TMP_CNT_VL": {
                "read_only": True
            },
            "ID_MRHRC_TMP_CNT": {
                "read_only": True
            }
        }


class MerchandiseTemplateControlSerializer(serializers.ModelSerializer):
    '''MerchandiseTemplateControls Serializer'''

    customfield_values = MerchandiseTemplateControlValueSerializer(
        many=True, write_only=True)

    customformfield = serializers.SerializerMethodField(read_only=True)
    options = serializers.SerializerMethodField(read_only=True)

    def get_customformfield(self, obj):
        '''method to get customform field'''
        tp_list = CustomFormFieldRetriveSerializer(
            obj.ID_BA_CFF).data
        return tp_list

    def get_options(self, obj):
        '''method to get Merchandise Template Control Value'''
        tp_list = MerchandiseTemplateControlValueSerializer(
            obj.taxonomy_template_control.filter(isdeleted=False).all().order_by('ID_MRHRC_TMP_CNT_VL'), many=True).data
        return tp_list

    def update(self, instance, validated_data):
        customfields_value_data = validated_data.pop('customfield_values')
        request = self.context['request']
        current_user = request.user
        instance.merchandisetemplatecontroldescription = validated_data.get(
            'merchandisetemplatecontroldescription', instance.merchandisetemplatecontroldescription)
        instance.ID_BA_CFF = validated_data.get(
            'ID_BA_CFF', instance.ID_BA_CFF)
        instance.ismandatory = validated_data.get(
            'ismandatory', instance.ismandatory)
        instance.isfilterable = validated_data.get(
            'isfilterable', instance.isfilterable)
        instance.ishidden = validated_data.get('ishidden', instance.ishidden)
        instance.isvalidation = validated_data.get(
            'isvalidation', instance.isvalidation)
        instance.updatedby = current_user.id
        instance.save()
        logger.info(
            "Merchandise Template Controls Instance Update: %s", instance)
        for customfields_value in customfields_value_data:
            customfields_value['ID_MRHRC_TMP_CNT'] = instance
            try:
                obj = MerchandiseTemplateControlValue.objects.get(
                    ID_MRHRC_TMP_CNT=instance.ID_MRHRC_TMP_CNT, ID_BA_CFF_VAL=customfields_value['ID_BA_CFF_VAL'])
                obj.merchandisetemplatecontrol_value = customfields_value.get(
                    'merchandisetemplatecontrol_value', obj.merchandisetemplatecontrol_value)
                obj.isdefault = customfields_value.get(
                    'isdefault', obj.isdefault)
                obj.save()
            except MerchandiseTemplateControlValue.DoesNotExist:
                MerchandiseTemplateControlValue.objects.create(
                    **customfields_value)
        return instance

    class Meta:
        model = MerchandiseTemplateControls
        fields = ["ID_MRHRC_TMP_CNT", "ID_MRHRC_TMP",
                  "merchandisetemplatecontroldescription", "ID_BA_CFF", "ismandatory", "isfilterable", "ishidden", "isvalidation", "customfield_values", "customformfield", "options"]
        extra_kwargs = {
            "ID_MRHRC_TMP": {
                "read_only": True
            }
        }


class MerchandiseTemplateCreateSerializer(serializers.ModelSerializer):
    '''Template create update'''
    customfields = MerchandiseTemplateControlSerializer(
        many=True, write_only=True)

    def create(self, validated_data):
        customfields_data = validated_data.pop(
            'customfields')
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        template_instance = MerchandiseTemplate.objects.create(
            **validated_data)
        logger.info("Merchandise Template Instance Create: %s",
                    template_instance)
        for customfields in customfields_data:
            customfields_value_data = customfields.pop(
                'customfield_values')
            customfields['ID_MRHRC_TMP'] = template_instance
            customfields['createdby'] = current_user.id
            control_instance = MerchandiseTemplateControls.objects.create(
                **customfields)
            logger.info(
                "Merchandise Template Control Instance Create: %s", control_instance)
            for customfields_value in customfields_value_data:
                customfields_value['ID_MRHRC_TMP_CNT'] = control_instance
                MerchandiseTemplateControlValue.objects.create(
                    **customfields_value)
        return template_instance

    def update(self, instance, validated_data):
        customfields_data = validated_data.pop(
            'customfields')
        request = self.context['request']
        current_user = request.user
        instance.merchandisetemplatename = validated_data.get(
            'merchandisetemplatename', instance.merchandisetemplatename)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.ID_MRHRC_TMP_TYP = validated_data.get(
            'ID_MRHRC_TMP_TYP', instance.ID_MRHRC_TMP_TYP)
        instance.status = validated_data.get('status', instance.status)
        instance.updatedby = current_user.id
        instance.save()
        logger.info("Merchandise Template Instance Update: %s", instance)
        for customfields in customfields_data:
            customfields_value_data = customfields.pop(
                'customfield_values')
            customfields['ID_MRHRC_TMP'] = instance
            customfields['createdby'] = current_user.id
            control_instance = MerchandiseTemplateControls.objects.create(
                **customfields)
            logger.info(
                "Merchandise Template Control Instance Create: %s", control_instance)
            for customfields_value in customfields_value_data:
                customfields_value['ID_MRHRC_TMP_CNT'] = control_instance
                MerchandiseTemplateControlValue.objects.create(
                    **customfields_value)
        return instance

    class Meta:
        model = MerchandiseTemplate
        fields = ["ID_MRHRC_TMP", "merchandisetemplatename", "description",
                  "ID_MRHRC_TMP_TYP", "status", "customfields"]


class MerchandiseTemplateRetriveSerializer(serializers.ModelSerializer):
    '''CustomFormField Retrive serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    ID_MRHRC_TMP_TYP = serializers.SerializerMethodField(read_only=True)
    controls = serializers.SerializerMethodField(read_only=True)

    def get_controls(self, obj):
        '''method to get assigned controls'''
        tp_list = MerchandiseTemplateControlSerializer(
            obj.taxonomy_template.filter(isdeleted=False).all().order_by('ID_MRHRC_TMP_CNT'), many=True).data
        return tp_list

    def get_ID_MRHRC_TMP_TYP(self, obj):
        '''method to get template type'''
        tp_list = MerchandiseTemplateTypeListSerializer(
            obj.ID_MRHRC_TMP_TYP).data
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
        model = MerchandiseTemplate
        fields = ["ID_MRHRC_TMP", "merchandisetemplatename", "description",
                  "ID_MRHRC_TMP_TYP", "status", "createdby",
                  "createddate", "updatedby", "updateddate", "controls"]


class MerchandiseTemplateListSerializer(serializers.ModelSerializer):
    '''MerchandiseTemplateType List'''
    class Meta:
        model = MerchandiseTemplate
        fields = '__all__'


class MerchandiseTemplateTypeListSerializer(serializers.ModelSerializer):
    '''MerchandiseTemplateType List'''
    class Meta:
        model = MerchandiseTemplateType
        fields = '__all__'


class CustomFormFieldTypeListSerializer(serializers.ModelSerializer):
    '''CustomFormFieldType'''
    class Meta:
        model = CustomFormFieldType
        fields = '__all__'


class CustomFormFieldValueSerializer(serializers.ModelSerializer):
    '''CustomFormFieldValue Serializer'''
    class Meta:
        model = CustomFormFieldValue
        fields = ["customformfield_value", "isdefault"]


class CustomFormFieldCreateSerializer(serializers.ModelSerializer):
    '''CustomFormField create update'''
    customformfield_values = CustomFormFieldValueSerializer(
        many=True, write_only=True)

    def create(self, validated_data):
        customformfield_values_data = validated_data.pop(
            'customformfield_values')
        request = self.context['request']
        current_user = request.user
        validated_data['createdby'] = current_user.id
        formfield_instance = CustomFormField.objects.create(**validated_data)
        logger.info("Custom Form Field Instance Create: %s",
                    formfield_instance)
        for customformfield_values in customformfield_values_data:
            customformfield_values['ID_BA_CFF'] = formfield_instance
            CustomFormFieldValue.objects.create(**customformfield_values)
        return formfield_instance

    class Meta:
        model = CustomFormField
        fields = ["ID_BA_CFF", "customformfield_name", "customformfield_description",
                  "ID_BA_CFF_TYP", "customformfield_label", "customformfield_values"]


class CustomFormFieldValueListSerializer(serializers.ModelSerializer):
    '''CustomFormFieldValue List Serializer'''
    class Meta:
        model = CustomFormFieldValue
        fields = ["ID_BA_CFF_VAL", "customformfield_value", "isdefault"]


class CustomFormFieldRetriveSerializer(serializers.ModelSerializer):
    '''CustomFormField Retrive serializer'''
    createdby = serializers.SerializerMethodField(read_only=True)
    updatedby = serializers.SerializerMethodField(read_only=True)
    customformfieldtype = serializers.SerializerMethodField(read_only=True)
    customformfield_values = serializers.SerializerMethodField(
        read_only=True)

    def get_customformfield_values(self, obj):
        '''method to get assigned values'''
        tp_list = CustomFormFieldValueListSerializer(
            obj.customformfieldvalue_set.filter(isdeleted=False).all().order_by('ID_BA_CFF_VAL'), many=True).data
        return tp_list

    def get_customformfieldtype(self, obj):
        '''method to get assigned customformfieldtype'''
        tp_list = CustomFormFieldTypeListSerializer(obj.ID_BA_CFF_TYP).data
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
        model = CustomFormField
        fields = ["ID_BA_CFF", "customformfield_name", "customformfield_description",
                  "customformfield_label", "status", "createdby",
                  "createddate", "updatedby", "updateddate", "customformfieldtype", "customformfield_values"]


class CustomFormFieldvalueCreateSerializer(serializers.ModelSerializer):
    '''CustomFormField Value create update'''

    class Meta:
        model = CustomFormFieldValue
        fields = ["ID_BA_CFF_VAL", "ID_BA_CFF", "customformfield_value",
                  "isdefault"]


class CustomFormFieldvalueAddSerializer(serializers.ModelSerializer):
    '''CustomFormField create update'''
    customformfield_values = CustomFormFieldvalueCreateSerializer(
        many=True, write_only=True)

    class Meta:
        model = CustomFormFieldValue
        fields = ["customformfield_values"]
