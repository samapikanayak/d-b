'''views for position APIs'''
import logging
from rest_framework import (
    mixins,
    generics,
    views,
    permissions,
    response,
    status
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .seriailizers import PositionSerializer, Position, PositionstatusSerializer


logger = logging.getLogger(__name__)

position_response_schema_dict = {
    "200": PositionSerializer,
    "401": openapi.Response(
        description="Data not found"
    )
}


class PositionListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    '''Position List Create API'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ID_PST', 'status']

    @swagger_auto_schema(tags=['Position'], operation_description="position List", operation_summary="position List")
    def get(self, request):
        '''mixin list method called'''
        position_id = request.GET.get('ID_PST')
        if position_id is None:
            return self.list(request)
        else:
            try:
                queryset = Position.objects.get(
                    ID_PST=position_id)
                response_data = PositionSerializer(queryset).data
            except Position.DoesNotExist:
                response_data = {"detail": "No data found"}
            return response.Response(response_data)

    @swagger_auto_schema(tags=['Position'], operation_description="Position List", operation_summary="Position List", responses=position_response_schema_dict)
    def list(self, request, *args, **kwargs):
        respons = super().list(request, args, kwargs)
        respons.data['columns'] = {
            "ID_PST": "Id", "NM_TTL": "Position Name", "DE_PST": "Position Description",
            "ID_LCN": "Work Location Id", "ID_JOB": "Job Id", "department_id": "Department Id",
            "department_name": "Department", "createddate": "Created Date & Time", "status": "Status", "updatedby": "Modified By", "MDF_DT": "Updated Date"
        }
        respons.data['column_type'] = {
            "ID_PST": "int", "NM_TTL": "str",  "DE_PST": "str", "createddate": "Datetime",
            "status": "status", "ID_LCN": "int", "ID_JOB": "int", "department_id": "int",
            "updatedby": "str", "start_date": "Datetime", "end_date": "Datetime"
        }

        return respons

    @swagger_auto_schema(tags=['Position'], operation_description="Position Create", operation_summary="Position Create", responses=position_response_schema_dict)
    def post(self, request):
        '''List of Position'''
        logger.info("Position create, User : %s ,Post Data : %s ",
                    request.user, request.data)
        return self.create(request)


class PositionRetriveUpdate(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    '''Item Tender Detail'''
    serializer_class = PositionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "positionId"

    def get_queryset(self):
        '''retrive method'''
        positionId = self.kwargs.get(self.lookup_url_kwarg)
        query = Position.objects.filter(
            ID_PST=positionId)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    @swagger_auto_schema(tags=['Position'], operation_description="Position Update", operation_summary="Position Update", responses=position_response_schema_dict)
    def put(self, request, *args, **kwargs):
        '''update of position'''
        return self.update(request, *args, **kwargs)



class PositionStatusUpdate(views.APIView):
    '''position status update'''

    def validate_ids(self, id_list):
        '''position validate id'''
        for each_id in id_list:
            try:
                Position.objects.get(ID_PST=each_id)
            except (Position.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Position'], operation_description="Position multiple status update",
                         operation_summary="Position multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Position Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='department status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''position multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = Position.objects.get(ID_PST=each_id)
                obj.status = status_val
                obj.save()
                instances.append(obj)
            serializer = PositionstatusSerializer(instances, many=True)
            return response.Response(serializer.data, *args, **kwargs)
        else:
            response_data = {}
            response_data["message"] = "Invalid Id"
            return response.Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class PositionMultipleDelete(views.APIView):
    '''position delete'''

    def validate_ids(self, id_list):
        '''position validate id'''
        for each_id in id_list:
            try:
                Position.objects.get(ID_PST=each_id)
            except (Position.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Position'], operation_description="Position multiple delete",
                         operation_summary="Position multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Position Id')),
        }, required=['ids']
    ))

    def delete(self, request):
        '''position multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                Position.objects.filter(ID_PST=each_id).delete()
            return response.Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = {}
            response_data["message"] = "Invalid Id"
            return response.Response(response, status=status.HTTP_400_BAD_REQUEST)
