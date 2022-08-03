'''pos view'''
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
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from pos_department.models import POSDepartment
from pos_department.serializers import POSDepartmentCreateSerializer, POSDepartmentRetriveSerializer, POSDepartmentListSerializer, POSDepartmentSerializer

logger = logging.getLogger(__name__)


class POSDepartmentCreate(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''POSDepartment create and list'''
    queryset = POSDepartment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_DPT_PS', 'status']
    search_fields = ['NM_DPT_PS']
    ordering_fields = '__all__'
    ordering = ['ID_DPT_PS']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return POSDepartmentSerializer
        return POSDepartmentCreateSerializer

    @swagger_auto_schema(tags=['POS Department'], operation_description="Add POS Department", operation_summary="POS Department add")
    def post(self, request, *args, **kwargs):
        '''POS Department create'''
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {"status": "Status", "pos_code": "POS Department ID", "NM_DPT_PS": "POS Department Name",
                                    "ID_DPT_PS_PRNT": "Parent POS Department ID",
                                    "item_selling_rule": "Item Selling Rule", "b_unit_group": "Business Unit Group",
                                    "createdby": "Created By", "createddate": "Date Created", "updatedby": "Modified By",
                                    "updateddate": "Date Modified"}
        response.data['column_type'] = {"status": "status", "pos_code": "str", "NM_DPT_PS": "str",
                                        "ID_DPT_PS_PRNT": "str",
                                        "item_selling_rule": "str", "b_unit_group": "str", "createdby": "str",
                                        "createddate": "date", "updatedby": "str", "updateddate": "date"}
        return response

    @swagger_auto_schema(tags=['POS Department'], operation_description="get POS Department list", operation_summary="POS Department list")
    def get(self, request, *args, **kwargs):
        '''POS Department list'''
        pos_dept_id = request.GET.get('ID_DPT_PS')
        if pos_dept_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = POSDepartment.objects.get(ID_DPT_PS=pos_dept_id)
            response_data = POSDepartmentRetriveSerializer(queryset)
            return Response(response_data.data)


pos_params = [
    openapi.Parameter("posId",
                      openapi.IN_PATH,
                      description="POS id",
                      type=openapi.TYPE_INTEGER
                      )
]


class POSDepartmentRetrieveUpdate(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    '''POSDepartment retrive update'''
    lookup_url_kwarg = "posId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        posid = self.kwargs.get(self.lookup_url_kwarg)
        query = POSDepartment.objects.filter(
            ID_DPT_PS=posid)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        qfilter = {}
        obj = get_object_or_404(queryset, **qfilter)
        return obj

    def get_serializer_class(self):
        return POSDepartmentCreateSerializer

    @swagger_auto_schema(tags=['POS Department'], manual_parameters=pos_params,
                         operation_description="update POS Department", operation_summary="POS Department update")
    def put(self, request, *args, **kwargs):
        '''POS Department update'''
        return self.update(request, *args, **kwargs)


class POSDepartmentstatusUpdateMultipleView(APIView):
    '''POSDepartment multiple status update'''

    def validate_ids(self, id_list):
        '''POSDepartment validate id'''
        for each_id in id_list:
            try:
                POSDepartment.objects.get(ID_DPT_PS=each_id)
            except (POSDepartment.DoesNotExist, ValidationError):
                logger.exception(POSDepartment.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['POS Department'], operation_description="multiple status update POS Department",
                         operation_summary="POS Department multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='POS Department Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='POS Department status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''POS Department multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        current_user = request.user
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = POSDepartment.objects.get(ID_DPT_PS=each_id)
                obj.status = status_val
                obj.updatedby = current_user.id
                obj.save()
                instances.append(obj)
                logger.info("POS Department Status Update, Id : %s ,Status : %s ",
                            each_id, status_val)
            serializer = POSDepartmentListSerializer(instances, many=True)
            return Response(serializer.data)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class POSDepartmentDeleteMultipleView(APIView):
    '''POSDepartment multiple status update'''

    def validate_ids(self, id_list):
        '''POSDepartment validate id'''
        for each_id in id_list:
            try:
                POSDepartment.objects.get(ID_DPT_PS=each_id)
            except (POSDepartment.DoesNotExist, ValidationError):
                logger.exception(POSDepartment.DoesNotExist)
                return False
        return True

    @swagger_auto_schema(tags=['POS Department'], operation_description="multiple delete POS Department", operation_summary="POS Department multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='POS Department Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''POS Department multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                obj = POSDepartment.objects.get(ID_DPT_PS=each_id)
                obj.delete()
                logger.info("POS Department Delete, Id : %s",
                            each_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
