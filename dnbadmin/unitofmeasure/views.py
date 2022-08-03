''' Unit Of Measurement Views '''
import logging
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import UnitOfMeasure, UnitOfMeasureConversion
from .serializers import UomCreateSerializer, UomUpdateSerializer, UomSerializerGet

# Create your views here.
logger = logging.getLogger(__name__)


uom_response_schema = {
    "201": openapi.Response(
        description="Created Successfully",
    ),
    "200": openapi.Response(
        description="Unit Already Exists",
    ),
    "400": openapi.Response(
        description="Bad Request"
    )
}


class UnitOfMeasureGet(ListModelMixin, GenericAPIView):
    ''' Get Unit of Measure '''
    permission_classes = (IsAuthenticated,)
    serializer_class = UomCreateSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_UOM', 'STATUS_UOM']
    search_fields = ['CD_UOM', 'TY_UOM',
                     'NM_UOM', 'STATUS_UOM']
    ordering_fields = '__all__'
    ordering = ['ID_UOM']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UomCreateSerializer
        return UomSerializerGet

    def get_queryset(self):
        query = UnitOfMeasure.objects.all()
        return query

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "STATUS_UOM": "Status", "CD_UOM": "Unit Name", "CREATED_AT": "Created Date & Time"}
        response.data['column_type'] = {
            "STATUS_UOM": "status", "CD_UOM": "str", "CREATED_AT": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Unit Of Measure'], operation_description="Get all unit of measure", operation_summary="Get unit of measure")
    def get(self, request, *args, **kwargs):
        ''' Unit Of Measure List '''
        uom_id = request.GET.get('ID_UOM')
        logger.info("Unit Of Measure Id : %s", uom_id)
        if uom_id is None:
            logger.info("Unit Of Measure ID None")
            return self.list(request, *args, **kwargs)
        else:
            logger.info("Unit Of Measure ID  Not None")
            queryset = UnitOfMeasure.objects.get(ID_UOM=uom_id)
            response_data = UomCreateSerializer(queryset)
            return Response(response_data.data)

    @swagger_auto_schema(tags=['Unit Of Measure'], operation_description="Here we create unit of measure", operation_summary="create unit of measure", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uom_conversion': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                "MO_UOM_CVN": openapi.Schema(type=openapi.TYPE_NUMBER, description='Unit of measure factor'),
                "DE_CVN_RUL": openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure conversion rule'),
                "ID_CVN_UOM_FM": openapi.Schema(type=openapi.TYPE_INTEGER, description='Unit of measure conversion from'),
                "ID_CVN_UOM_TO": openapi.Schema(type=openapi.TYPE_INTEGER, description='Unit of measure conversion to'),
            })),

            "CD_UOM": openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure code'),
            "TY_UOM": openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure type'),
            "NM_UOM": openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure name'),
            "DE_UOM": openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure desscription'),
            "STATUS_UOM": openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure status'),
        }, required=['CD_UOM']
    ), responses=uom_response_schema)
    def post(self, request):
        ''' Black List Refresh Token '''
        response = {}
        http_status = None
        message = None
        try:
            with transaction.atomic():
                serializer = self.serializer_class(data=request.data)
                unit_code = request.data['CD_UOM']
                if serializer.is_valid():
                    result = serializer.save()
                    logger.info("Create Response : %s", result)
                    if result[1]:
                        http_status = status.HTTP_201_CREATED
                        message = "Unit Created Successfully"
                        response['message'] = message
                    else:
                        http_status = status.HTTP_200_OK
                        message = f"{unit_code} already exists"
                        response['message'] = message
                else:
                    http_status = status.HTTP_400_BAD_REQUEST
                    message = "Invalid Data"
                    response['message'] = message

                return Response(response, status=http_status)
        except Exception as exp:
            logger.exception(exp)
            message = ""
            response['message'] = message
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


uom_params = [
    openapi.Parameter("unitofmeasureId",
                      openapi.IN_PATH,
                      description="Unit Of Measure id",
                      type=openapi.TYPE_INTEGER
                      )
]

uom_update_response_schema = {
    "200": openapi.Response(
        description="Successfully Updated",
    ),
    "400": openapi.Response(
        description="Bad Request"
    )
}


class UnitOfMeasureUpdate(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    ''' Update Unit of Measure '''
    permission_classes = (IsAuthenticated,)
    serializer_class = UomUpdateSerializer
    lookup_url_kwarg = "unitofmeasureId"

    def get_queryset(self):
        uom_id = self.kwargs.get(self.lookup_url_kwarg)
        query = UnitOfMeasure.objects.filter(
            ID_UOM=uom_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    @swagger_auto_schema(tags=['Unit Of Measure'], manual_parameters=uom_params, request_body=UomUpdateSerializer,
                         operation_description="update unit of measure", operation_summary="Unit of measure update", responses=uom_update_response_schema)
    def put(self, request, *args, **kwargs):
        '''Unit Of Measure setting update'''
        logger.info("Request Data : %s", request)
        try:
            with transaction.atomic():
                uom_id = self.kwargs.get(self.lookup_url_kwarg)
                logger.info("UOM ID : %s", uom_id)
                data = request.data
                response = {}
                serializer_data = UomUpdateSerializer(data=data)
                data_valid = serializer_data.is_valid()
                logger.info("Data Valid : %s", data_valid)
                if data_valid:
                    uom_convs_data = data.pop('uom_conversion')
                    logger.info("Uom Conversion Data : %s", uom_convs_data)
                    logger.info("Uom Data : %s", data)
                    UnitOfMeasure.objects.filter(ID_UOM=uom_id).update(**data)
                    uom_conv_obj = UnitOfMeasureConversion.objects.filter(
                        ID_CVN_UOM_FM=uom_id).delete()
                    logger.info("UOM Conv Obj : %s", uom_conv_obj)
                    for uom_conv in uom_convs_data:
                        logger.info("Insert New Conversion")
                        from_instance = UnitOfMeasure.objects.get(
                            ID_UOM=uom_id)
                        to_instance = UnitOfMeasure.objects.get(
                            ID_UOM=uom_conv['ID_CVN_UOM_TO'])
                        uom_conv['ID_CVN_UOM_FM'] = from_instance
                        uom_conv['ID_CVN_UOM_TO'] = to_instance
                        UnitOfMeasureConversion.objects.create(**uom_conv)
                    response['message'] = "Successfully Updated"
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response['message'] = "Invalid Data"
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exp:
            logger.exception(exp)
            response = {}
            response['message'] = "Error Encountered"
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnitOfMeasureMultipleStatusUpdate(APIView):
    '''Unit of measure multiple status update'''
    permission_classes = (IsAuthenticated,)

    def validate_ids(self, id_list):
        '''unit of measure validate uom id'''
        for uom_id in id_list:
            try:
                UnitOfMeasure.objects.get(ID_UOM=uom_id)
            except (UnitOfMeasure.DoesNotExist, ValidationError):
                return False
        return True

    multiple_update_response_schema = {
        "200": openapi.Response(
            description="Status Successfully Updated",
        ),
        "400": openapi.Response(
            description="Bad Request"
        )
    }

    @swagger_auto_schema(tags=['Unit Of Measure'], operation_description="unit of measure multiple status update",
                         operation_summary="Unit of measure multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids',
                                  items=openapi.Items(type=openapi.TYPE_INTEGER, description='Unit of measure Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measure status (A/I)'),
        }, required=['ids', 'status']
    ), responses=multiple_update_response_schema)
    def put(self, request):
        '''Unit of measure multiple status update'''
        uom_id_list = request.data['ids']
        uom_status = request.data['status']
        chk_stat = self.validate_ids(id_list=uom_id_list)
        if chk_stat:
            instances = []
            for uom_id in uom_id_list:
                obj = UnitOfMeasure.objects.get(ID_UOM=uom_id)
                obj.STATUS_UOM = uom_status
                obj.save()
                instances.append(obj)
            response = {}
            response["message"] = "Status Successfully Updated"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {}
            response["message"] = "Invalid Unit of Measure Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    multiple_delete_response_schema = {
        "200": openapi.Response(
            description="Item Successfully Deleted",
        ),
        "400": openapi.Response(
            description="Bad Request"
        )
    }

    @swagger_auto_schema(tags=['Unit Of Measure'], operation_description="unit of measure multiple delete", operation_summary="Unit of measure multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids', items=openapi.Items(type=openapi.TYPE_INTEGER, description='Unit of measure Id')),
        }, required=['ids']
    ))
    def delete(self, request):
        '''Unit of measure multiple status update'''
        uom_id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=uom_id_list)
        response = {}
        if chk_stat:
            for uom_id in uom_id_list:
                obj = UnitOfMeasure.objects.get(ID_UOM=uom_id)
                obj.delete()
            response["message"] = "Item Successfully Deleted"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["message"] = "Invalid Unit of Measure Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
