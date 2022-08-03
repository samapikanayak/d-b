'''Department views'''
import logging
from rest_framework import (
    mixins,
    generics,
    response,
    views,
    permissions,
    filters,
    status
)
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import Department, DepartmentSerializer, DepartmentstatusSerializer

logger = logging.getLogger(__name__)

class DepartmentListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    '''Department List Create View'''
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department_id', 'status']
    search_fields = ['name']
    ordering_fields = '__all__'
    ordering = ['department_id']
    @swagger_auto_schema(
                tags=['Department'], operation_description="Add Department",  operation_summary="Department Create"
    )
    def post(self, request):
        '''department create'''
        logger.info("Department create, User : %s ,Post Data : %s ",
                    request.user, request.data)
        return self.create(request)

    @swagger_auto_schema(
                tags=['Department'], operation_description="List Department",  operation_summary="Department List"
    )
    def list(self, request, *args, **kwargs):
        respons = super().list(request, args, kwargs)
        respons.data['columns'] = {
                "department_id": "Id", "name": "Department Name",
                "description": "Department Description",
                "business_unit_group_code": "Business Unit Group Id",
                "parent_department_id": "Parent Department Id","createddate": "Created Date & Time", "status": "Status", "updatedby": "Modified By"
        }
        respons.data['column_type'] = {
            "department_id": "int", "name": "str",  "description": "str", "createddate": "Datetime", "status": "status", "business_unit_group_code": "int", "updatedby": "str"}

        return respons

    @swagger_auto_schema(tags=['Department'], operation_description="department List", operation_summary="Department List")
    def get(self, request):
        '''mixin list method called'''
        department_id = request.GET.get('department_id')
        if department_id is None:
            return self.list(request)
        else:
            try:
                queryset = Department.objects.get(
                    department_id=department_id)
                response_data = DepartmentSerializer(queryset).data
            except Department.DoesNotExist:
                response_data = {"detail": "No data found"}
            return response.Response(response_data)



class DepartmentRetriveUpdate(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    '''Department Detail'''
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "departmentId"

    def get_queryset(self):
        '''retrive method'''
        departmentId = self.kwargs.get(self.lookup_url_kwarg)
        query = Department.objects.filter(
            department_id=departmentId)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    @swagger_auto_schema(tags=['Department'], operation_description="Department Update", operation_summary="Department Update")
    def put(self, request, *args, **kwargs):
        '''department update method'''
        logger.info("Department Update, ID : %s ,User : %s ,PUT Data : %s ",
                    self.kwargs.get(self.lookup_url_kwarg), request.user, request.data)
        return self.update(request, *args, **kwargs)

class DepartmentstatusUpdateMultipleView(views.APIView):
    '''department multiple status update'''

    def validate_ids(self, id_list):
        '''department validate id'''
        for each_id in id_list:
            try:
                Department.objects.get(department_id=each_id)
            except (Department.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Department'], operation_description="Department multiple status update",
                         operation_summary="Department multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Department Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='department status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request):
        '''department multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = Department.objects.get(department_id=each_id)
                obj.status = status_val
                obj.save()
                instances.append(obj)
            serializer = DepartmentstatusSerializer(instances, many=True)
            return response.Response(serializer.data)
        else:
            response_data = {}
            response_data["message"] = "Invalid Id"
            return response.Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDeleteMultipleView(views.APIView):
    '''Department multiple delete'''

    def validate_ids(self, id_list):
        '''deaprtment validate id'''
        for each_id in id_list:
            try:
                Department.objects.get(department_id=each_id)
            except (Department.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Department'], operation_description="department multiple delete", operation_summary="department multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Department Id'))
        }, required=['ids']
    ))
    def delete(self, request):
        '''department multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                Department.objects.filter(department_id=each_id).delete()
            return response.Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {}
            response_data["message"] = "Invalid Id"
            return response.Response(response, status=status.HTTP_400_BAD_REQUEST)
