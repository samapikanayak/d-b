'''work schedule view'''
import logging
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from workerschedule.models import TimeGroup
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from workerschedule.serializers import TimeGroupCreateSerializer, TimeGroupRetriveSerializer, TimeGroupSerializer, TimeGroupListSerializer

logger = logging.getLogger(__name__)


class WorkScheduleCreate(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''work schedule create and list'''
    queryset = TimeGroup.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_GP_TM', 'status']
    search_fields = ['DE_GP_TM']
    ordering_fields = '__all__'
    ordering = ['ID_GP_TM']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TimeGroupListSerializer
        return TimeGroupCreateSerializer

    @swagger_auto_schema(tags=['Business Hours'], operation_description="Add Business Hours", operation_summary="Business Hours add")
    def post(self, request, *args, **kwargs):
        '''Work Availability create'''
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "status": "Status", "NM_GP_TM": "Schedule Name",  "weekdays": "Weekday", "createddate": "Created Date & Time"}
        response.data['column_type'] = {
            "status": "status", "NM_GP_TM": "str",  "weekdays": "str", "createddate": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Business Hours'], operation_description="get Business Hours list", operation_summary="Business Hours list")
    def get(self, request, *args, **kwargs):
        '''Work Availability list'''
        tm_gp_id = request.GET.get('ID_GP_TM')
        logger.info("Time Group Id : %s", tm_gp_id)
        if tm_gp_id is None:
            return self.list(request, *args, **kwargs)
        else:
            logger.info("Global Setting ID  Not None")
            queryset = TimeGroup.objects.get(ID_GP_TM=tm_gp_id)
            response_data = TimeGroupRetriveSerializer(queryset)
            return Response(response_data.data)


wschedule_params = [
    openapi.Parameter("bhourId",
                      openapi.IN_PATH,
                      description="Business Hours id",
                      type=openapi.TYPE_INTEGER
                      )
]


class WorkScheduleRetrieveUpdate(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    '''work schedule retrive update'''
    lookup_url_kwarg = "bhourId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gsetting_id = self.kwargs.get(self.lookup_url_kwarg)
        query = TimeGroup.objects.filter(
            ID_GP_TM=gsetting_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        obj = get_object_or_404(queryset, **filter)
        return obj

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TimeGroupRetriveSerializer
        return TimeGroupCreateSerializer

    @swagger_auto_schema(tags=['Business Hours'], manual_parameters=wschedule_params,
                         operation_description="update Business Hours", operation_summary="Business Hours update")
    def put(self, request, *args, **kwargs):
        '''work schedule update'''
        return self.update(request, *args, **kwargs)


class WorkSchedulestatusUpdateMultipleView(APIView):
    '''work schedule multiple status update'''

    def validate_ids(self, id_list):
        '''work schedule validate id'''
        for each_id in id_list:
            try:
                TimeGroup.objects.get(ID_GP_TM=each_id)
            except (TimeGroup.DoesNotExist, ValidationError):
                logger.exception(TimeGroup.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Business Hours'], operation_description="multiple status update Business Hours",
                         operation_summary="Business Hours multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Business Hours Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Business Hours status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''Business Hours multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        current_user = request.user
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = TimeGroup.objects.get(ID_GP_TM=each_id)
                obj.status = status_val
                obj.updatedby = current_user.id
                obj.save()
                instances.append(obj)
                logger.info("Business Hours Status Update, Id : %s ,Status : %s ",
                            each_id, status_val)
            serializer = TimeGroupSerializer(instances, many=True)
            return Response(serializer.data)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class WorkScheduleDeleteMultipleView(APIView):
    '''work schedule multiple status update'''

    def validate_ids(self, id_list):
        '''work schedule validate id'''
        for each_id in id_list:
            try:
                TimeGroup.objects.get(ID_GP_TM=each_id)
            except (TimeGroup.DoesNotExist, ValidationError):
                logger.exception(TimeGroup.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Business Hours'], operation_description="multiple delete Business Hours", operation_summary="Business Hours multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Business Hours Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''Business Hours multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                t_group = TimeGroup.objects.get(ID_GP_TM=each_id)
                for timeperiod in t_group.timegrouptimeperiod_set.all():
                    timeperiod.ID_PD_TM.delete()
                t_group.delete()
                logger.info("Business Hours Delete, Id : %s",
                            each_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
