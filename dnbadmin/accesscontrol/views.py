''' Accesscontrol Views File '''
import logging
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Resource, WorkGroup
from .serializers import ResourceSerializer, WorkGroupSerializer, WorkGroupCreateSerializer, WorkGroupRetriveSerializer, WorkGroupUpdateSerializer

# Create your views here.
logger = logging.getLogger(__name__)

resource_response_schema = {
    "200": openapi.Response(
        description="Permission Resource List",
        examples={
            "application/json": [{
                "ID_RS": "Resource Id",
                "DE_RS": "Resource Name",
                "display_order": 0,
                "menu_url": "Menu URL",
                "is_visible_menu": "This Resource Visible or Not",
                "ID_RS_PRNT": "Parent Resource Id"
            }]
        }
    )
}


class PermissionResource(APIView):
    ''' Permission Resource List '''
    permission_classes = [AllowAny]
    pagination_class = None

    @swagger_auto_schema(tags=['Permission'], operation_description="Get permission resource list", operation_summary="Resource list", responses=resource_response_schema)
    def get(self, request):
        ''' To get permission resource list'''
        resources = Resource.objects.all()
        serialzer = ResourceSerializer(resources, many=True)
        resource_list = serialzer.data
        return Response(resource_list)


workgroup_response_schema = {
    "201": openapi.Response(
        description="Successfully Created"

    ),
    "400": openapi.Response(
        description="Invalid Data"

    )
}


class WorkGroupResource(ListModelMixin, CreateModelMixin, GenericAPIView):
    ''' Work Group Resource '''
    permission_classes = [AllowAny]
    queryset = WorkGroup.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_GP_WRK', 'status']
    search_fields = ['DE_GP_WRK', 'status']
    ordering_fields = '__all__'
    ordering = ['ID_GP_WRK']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkGroupSerializer
        return WorkGroupCreateSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "status": "Status", "NM_GP_WRK": "Permission Set Name", "access_type": "Access Type", "business_units": "Business Unit", "welcome_screen": "Welcome Screen", "DE_GP_WRK": "Description"}
        response.data['column_type'] = {
            "status": "status", "NM_GP_WRK": "str", "access_type": "str", "business_units": "str", "welcome_screen": "str", "DE_GP_WRK": "str"}

        return response

    @swagger_auto_schema(tags=['Permission'], operation_description="Get permission work group list", operation_summary="Permission work group list")
    def get(self, request, *args, **kwargs):
        ''' To get permission resource list'''
        work_group_id = request.GET.get('ID_GP_WRK')
        logger.info("Work Group Id : %s", work_group_id)
        if work_group_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = WorkGroup.objects.get(ID_GP_WRK=work_group_id)
            response_data = WorkGroupRetriveSerializer(queryset)
            return Response(response_data.data)

    @swagger_auto_schema(tags=['Permission'], request_body=WorkGroupCreateSerializer, operation_description="Create Permission WorkerGroup", operation_summary="Create Permission WorkerGroup Resource", responses=workgroup_response_schema)
    def post(self, request, *args, **kwargs):
        ''' Create Work Group Resource '''
        try:
            response = {}
            with transaction.atomic():
                self.create(request, *args, **kwargs)
                response['message'] = "Successfully Created"
                return Response(response, status=status.HTTP_201_CREATED)

        except Exception as exp:
            print(exp)
            error = getattr(exp, "message", repr(exp))
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


workgroup_params = [
    openapi.Parameter("workgroupId",
                      openapi.IN_PATH,
                      description="Work Group Id",
                      type=openapi.TYPE_INTEGER
                      )
]


class WorkGroupUpdate(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    '''Operator retrive update'''
    lookup_url_kwarg = "workgroupId"
    permission_classes = [AllowAny]

    def get_queryset(self):
        workgroup_id = self.kwargs.get(self.lookup_url_kwarg)
        query = WorkGroup.objects.filter(
            ID_GP_WRK=workgroup_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        qfilter = {}
        obj = get_object_or_404(queryset, **qfilter)
        return obj

    def get_serializer_class(self):
        return WorkGroupUpdateSerializer

    @swagger_auto_schema(tags=['Permission'], manual_parameters=workgroup_params,
                         operation_description="update permission work group", operation_summary="permission work group update")
    def put(self, request, *args, **kwargs):
        '''Work Group update'''
        return self.update(request, *args, **kwargs)
