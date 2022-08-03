'''operator view'''
import logging

from accesscontrol.models import Operator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from operators.serializers import (OperatorCreateSerializer,
                                   OperatorListSerializer,
                                   OperatorRetriveSerializer,
                                   OperatorUpdateSerializer)

logger = logging.getLogger(__name__)


class OperatorCreate(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''Operator create and list'''
    queryset = Operator.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_OPR', 'status']
    search_fields = ['EMAIL_USR', 'NM_USR']
    ordering_fields = '__all__'
    ordering = ['ID_OPR']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OperatorListSerializer
        return OperatorCreateSerializer

    @swagger_auto_schema(tags=['Operator'], operation_description="Add Operator", operation_summary="Operator add")
    def post(self, request, *args, **kwargs):
        '''Operator create'''
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {"status": "Status", "opr_code": "Operator ID", "NM_USR": "User Name",
                                    "EMAIL_USR": "Email Address",
                                    "b_unit_assigned": "Business Unit", "RS_TYP_OPR": "Resource Type",
                                    "createdby": "Created By", "createddate": "Date Created", "updatedby": "Modified By",
                                    "updateddate": "Date Modified"}

        response.data['column_type'] = {"status": "status", "opr_code": "str", "NM_USR": "str",
                                        "EMAIL_USR": "str",
                                        "b_unit_assigned": "str", "RS_TYP_OPR": "str",
                                        "createdby": "str", "createddate": "date", "updatedby": "str", "updateddate": "date"}
        return response

    @swagger_auto_schema(tags=['Operator'], operation_description="get Operator list", operation_summary="Operator list")
    def get(self, request, *args, **kwargs):
        '''Operator list'''
        opr_id = request.GET.get('ID_OPR')
        if opr_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = Operator.objects.get(ID_OPR=opr_id)
            response_data = OperatorRetriveSerializer(queryset)
            return Response(response_data.data)


pos_params = [
    openapi.Parameter("oprId",
                      openapi.IN_PATH,
                      description="Operator id",
                      type=openapi.TYPE_INTEGER
                      )
]


class OperatorRetrieveUpdate(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    '''Operator retrive update'''
    lookup_url_kwarg = "oprId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        oprid = self.kwargs.get(self.lookup_url_kwarg)
        query = Operator.objects.filter(
            ID_OPR=oprid)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        qfilter = {}
        obj = get_object_or_404(queryset, **qfilter)
        return obj

    def get_serializer_class(self):
        return OperatorUpdateSerializer

    @swagger_auto_schema(tags=['Operator'], manual_parameters=pos_params,
                         operation_description="update Operator", operation_summary="Operator update")
    def put(self, request, *args, **kwargs):
        '''Operator update'''
        return self.update(request, *args, **kwargs)


class OperatorstatusUpdateMultipleView(APIView):
    '''Operator multiple status update'''

    def validate_ids(self, id_list):
        '''Operator validate id'''
        for each_id in id_list:
            try:
                Operator.objects.get(ID_OPR=each_id)
            except (Operator.DoesNotExist, ValidationError):
                logger.exception(Operator.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Operator'], operation_description="multiple status update Operator",
                         operation_summary="Operator multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Operator Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Operator status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''Operator multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        current_user = request.user
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = Operator.objects.get(ID_OPR=each_id)
                obj.status = status_val
                obj.updatedby = current_user.id
                obj.save()
                instances.append(obj)
                logger.info("Operator Status Update, Id : %s ,Status : %s ",
                            each_id, status_val)
            serializer = OperatorListSerializer(instances, many=True)
            return Response(serializer.data)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OperatorDeleteMultipleView(APIView):
    '''Operator multiple status update'''

    def validate_ids(self, id_list):
        '''Operator validate id'''
        for each_id in id_list:
            try:
                Operator.objects.get(ID_OPR=each_id)
            except (Operator.DoesNotExist, ValidationError):
                logger.exception(Operator.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['Operator'], operation_description="multiple delete Operator", operation_summary="Operator multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Operator Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''Operator multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                obj = Operator.objects.get(ID_OPR=each_id)
                obj.delete()
                logger.info("Operator Delete, Id : %s",
                            each_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
