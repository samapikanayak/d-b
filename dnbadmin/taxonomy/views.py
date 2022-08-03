'''taxonomy modules view'''
import logging
from basics.models import (CustomFormField, CustomFormFieldType,
                           CustomFormFieldValue)
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from taxonomy.models import (MerchandiseTemplate, MerchandiseTemplateControls,
                             MerchandiseTemplateType)
from taxonomy.serializers import (CustomFormFieldCreateSerializer,
                                  CustomFormFieldRetriveSerializer,
                                  CustomFormFieldTypeListSerializer,
                                  CustomFormFieldvalueAddSerializer,
                                  MerchandiseTemplateControlSerializer,
                                  MerchandiseTemplateCreateSerializer,
                                  MerchandiseTemplateRetriveSerializer,
                                  MerchandiseTemplateTypeListSerializer,
                                  MerchandiseTemplateListSerializer,
                                  CustomFormFieldvalueCreateSerializer)

logger = logging.getLogger(__name__)


class MerchandiseTemplateCreate(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''MerchandiseTemplate create and list'''
    queryset = MerchandiseTemplate.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_MRHRC_TMP', 'status']
    search_fields = ['merchandisetemplatename']
    ordering_fields = '__all__'
    ordering = ['ID_MRHRC_TMP']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MerchandiseTemplateListSerializer
        return MerchandiseTemplateCreateSerializer

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="Add Taxonomy Template", operation_summary="Taxonomy Template add")
    def post(self, request, *args, **kwargs):
        '''Taxonomy Template create'''
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {"status": "Status", "merchandisetemplatename": "Template Name",
                                    "createddate": "Created Date & Time", "description": "Description"}
        response.data['column_type'] = {
            "status": "status", "merchandisetemplatename": "str", "createddate": "Datetime", "description": "str"}

        return response

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="get Taxonomy Template list", operation_summary="Taxonomy Template list")
    def get(self, request, *args, **kwargs):
        '''Taxonomy Template list'''
        temp_id = request.GET.get('ID_MRHRC_TMP')
        if temp_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = MerchandiseTemplate.objects.get(ID_MRHRC_TMP=temp_id)
            response_data = MerchandiseTemplateRetriveSerializer(queryset)
            return Response(response_data.data)


class MerchandiseTemplatestatusUpdateMultipleView(APIView):
    '''MerchandiseTemplate multiple status update'''

    def validate_ids(self, id_list):
        '''MerchandiseTemplate validate id'''
        for each_id in id_list:
            try:
                MerchandiseTemplate.objects.get(ID_MRHRC_TMP=each_id)
            except (MerchandiseTemplate.DoesNotExist, ValidationError):
                logger.exception(MerchandiseTemplate.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="multiple status update Taxonomy Template",
                         operation_summary="Taxonomy Template multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Taxonomy Master Template Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''MerchandiseTemplate multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        current_user = request.user
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = MerchandiseTemplate.objects.get(ID_MRHRC_TMP=each_id)
                obj.status = status_val
                obj.updatedby = current_user.id
                obj.save()
                instances.append(obj)
                logger.info("Taxonomy Template Status Update, Id : %s ,Status : %s ",
                            each_id, status_val)
            serializer = MerchandiseTemplateCreateSerializer(
                instances, many=True)
            return Response(serializer.data)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MerchandiseTemplateDeleteMultipleView(APIView):
    '''MerchandiseTemplate multiple status update'''

    def validate_ids(self, id_list):
        '''MerchandiseTemplate validate id'''
        for each_id in id_list:
            try:
                MerchandiseTemplate.objects.get(ID_MRHRC_TMP=each_id)
            except (MerchandiseTemplate.DoesNotExist, ValidationError):
                logger.exception(MerchandiseTemplate.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="multiple delete Taxonomy Template", operation_summary="Taxonomy Template multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Taxonomy Master Template Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''MerchandiseTemplate multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                obj = MerchandiseTemplate.objects.get(ID_MRHRC_TMP=each_id)
                obj.delete()
                logger.info("Taxonomy Template Delete, Id : %s",
                            each_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


template_params = [
    openapi.Parameter("taxtempId",
                      openapi.IN_PATH,
                      description="Taxonomy Template id",
                      type=openapi.TYPE_INTEGER
                      )
]


class MerchandiseTemplateRetrieveUpdate(UpdateModelMixin, GenericAPIView):
    '''MerchandiseTemplate retrive update'''
    lookup_url_kwarg = "taxtempId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gsetting_id = self.kwargs.get(self.lookup_url_kwarg)
        query = MerchandiseTemplate.objects.filter(
            ID_MRHRC_TMP=gsetting_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        obj = get_object_or_404(queryset, **filter)
        return obj

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MerchandiseTemplateRetriveSerializer
        return MerchandiseTemplateCreateSerializer

    @swagger_auto_schema(tags=['Taxonomy Template'], manual_parameters=template_params,
                         operation_description="update Taxonomy Template", operation_summary="Taxonomy Template update")
    def put(self, request, *args, **kwargs):
        '''MerchandiseTemplate update'''
        return self.update(request, *args, **kwargs)


template_control_params = [
    openapi.Parameter("cfield_Id",
                      openapi.IN_PATH,
                      description="Merchandise Template Controls id (ID_MRHRC_TMP_CNT)",
                      type=openapi.TYPE_INTEGER
                      )
]


class MerchandiseTemplateControlsRetrieveUpdate(UpdateModelMixin, GenericAPIView):
    '''MerchandiseTemplateControls retrive update'''
    lookup_url_kwarg = "cfield_Id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gsetting_id = self.kwargs.get(self.lookup_url_kwarg)
        query = MerchandiseTemplateControls.objects.filter(
            ID_MRHRC_TMP_CNT=gsetting_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        obj = get_object_or_404(queryset, **filter)
        return obj

    def get_serializer_class(self):
        return MerchandiseTemplateControlSerializer

    @swagger_auto_schema(tags=['Taxonomy Template'], manual_parameters=template_control_params,
                         operation_description="update Taxonomy Template custom fields", operation_summary="Taxonomy Template custom fields update")
    def put(self, request, *args, **kwargs):
        '''MerchandiseTemplateControls update'''
        return self.update(request, *args, **kwargs)


class MerchandiseTemplateControlsDeleteMultipleView(APIView):
    '''MerchandiseTemplateControls multiple delete'''

    def validate_ids(self, id_list):
        '''MerchandiseTemplateControls validate id'''
        for each_id in id_list:
            try:
                MerchandiseTemplateControls.objects.get(
                    ID_MRHRC_TMP_CNT=each_id)
            except (MerchandiseTemplateControls.DoesNotExist, ValidationError):
                logger.exception(MerchandiseTemplateControls.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="multiple delete Taxonomy Template custom fields",
                         operation_summary="Taxonomy Template custom fields multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids',
                                  items=openapi.Items(type=openapi.TYPE_STRING, description='Taxonomy Template custom fields Id (ID_MRHRC_TMP_CNT)'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''MerchandiseTemplateControls multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        current_user = request.user
        if chk_stat:
            for each_id in id_list:
                obj = MerchandiseTemplateControls.objects.get(
                    ID_MRHRC_TMP_CNT=each_id)
                obj.isdeleted = 1
                obj.updatedby = current_user.id
                obj.save()
                logger.info("MerchandiseTemplateControls Delete, Id : %s",
                            each_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CustomFormFieldCreate(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''CustomFormField create and list'''
    queryset = CustomFormField.objects.filter(isdeleted=False).all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_BA_CFF', 'customformfield_name']
    search_fields = ['customformfield_name', 'customformfield_description']
    ordering_fields = '__all__'
    ordering = ['-ID_BA_CFF']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomFormFieldRetriveSerializer
        return CustomFormFieldCreateSerializer

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="Add Custom Form Field", operation_summary="Custom Form Field add")
    def post(self, request, *args, **kwargs):
        '''CustomFormField create'''
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="get Custom Form Field list", operation_summary="Custom Form Field list")
    def get(self, request, *args, **kwargs):
        '''Custom Form Field list'''
        return self.list(request, *args, **kwargs)


class CustomFormFieldValueCreate(CreateModelMixin, GenericAPIView):
    '''CustomFormFieldValue create and list'''
    queryset = CustomFormFieldValue.objects.filter(isdeleted=False).all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_BA_CFF_VAL', 'customformfield_value']
    search_fields = ['customformfield_value']
    ordering_fields = '__all__'
    ordering = ['ID_BA_CFF_VAL']

    def get_serializer_class(self):
        return CustomFormFieldvalueAddSerializer

    def create(self, request, *args, **kwargs):
        data = request.data['customformfield_values']
        serialized = CustomFormFieldvalueCreateSerializer(
            data=data, many=isinstance(data, list))
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        response = {}
        response["message"] = "Unable to add"
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="Add Custom Form Field Value", operation_summary="Custom Form Field Value add")
    def post(self, request, *args, **kwargs):
        '''Custom Form Field Value create'''
        return self.create(request, *args, **kwargs)


class CustomFormFieldValueDeleteMultipleView(APIView):
    '''CustomFormFieldValue multiple delete'''

    def validate_ids(self, id_list):
        '''CustomFormFieldValue validate id'''
        for each_id in id_list:
            try:
                CustomFormFieldValue.objects.get(ID_BA_CFF_VAL=each_id)
            except (CustomFormFieldValue.DoesNotExist, ValidationError):
                logger.exception(CustomFormFieldValue.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="multiple delete Custom Form Field Value",
                         operation_summary="Custom Form Field Value multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Custom Form Field Value Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''Custom Form Field Value multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                CustomFormFieldValue.objects.filter(
                    ID_BA_CFF_VAL=each_id).delete()
                logger.info("Custom Form Field Value Delete, Id : %s",
                            each_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MerchandiseTemplateTypeList(ListModelMixin, GenericAPIView):
    '''MerchandiseTemplateType list'''
    queryset = MerchandiseTemplateType.objects.all()
    serializer_class = MerchandiseTemplateTypeListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_MRHRC_TMP_TYP']
    ordering_fields = '__all__'
    ordering = ['ID_MRHRC_TMP_TYP']

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="Taxonomy Template Type", operation_summary="Taxonomy Template Type")
    def get(self, request, *args, **kwargs):
        '''Taxonomy Template list'''
        return self.list(request, *args, **kwargs)


class CustomFormFieldTypeList(ListModelMixin, GenericAPIView):
    '''CustomFormFieldType list'''
    queryset = CustomFormFieldType.objects.all()
    serializer_class = CustomFormFieldTypeListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_BA_CFF_TYP']
    ordering_fields = '__all__'
    ordering = ['ID_BA_CFF_TYP']

    @swagger_auto_schema(tags=['Taxonomy Template'], operation_description="Taxonomy Template Form Field Type", operation_summary="Taxonomy Template Form Field Type")
    def get(self, request, *args, **kwargs):
        '''Taxonomy Template Form Field Type list'''
        return self.list(request, *args, **kwargs)
