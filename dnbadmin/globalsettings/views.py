"""global setting view"""
import logging
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from globalsettings.models import GlobalSetting
from globalsettings.serializers import GlobalSettingSerializer, GlobalSettingListSerializer, GlobalSettingUpdateSerializer, GlobalSettingstatusSerializer, ChangePasswordSerializer, GlobalSettingRetrieveSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend


logger = logging.getLogger(__name__)

password_change_response_schema_dict = {
    "200": openapi.Response(
        description="After Change Password Successfully",
        examples={
            "application/json": {
                "new_password": "New Password"
            }
        }
    ),
    "401": openapi.Response(
        description="No active account found with the given credentials"
    )
}


class ChangePassword(GenericAPIView):
    '''
    Change Password
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(tags=['Change-Password'], operation_description="Provide Your password", operation_summary="Change Password", request_body=ChangePasswordSerializer, responses=password_change_response_schema_dict)
    def post(self, request):
        '''
        return json data
        '''
        response = {}
        http_status = None
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        logger.info('user')
        logger.info(user.check_password("string"))

        user.set_password(serializer.data["new_password"])
        user.save()
        response["message"] = "Password changed successfully"
        http_status = status.HTTP_200_OK
        return Response(
            response,
            http_status
        )


class GlobalSettingCreate(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericAPIView):
    '''global setting create and list'''
    queryset = GlobalSetting.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_GB_STNG', 'status']
    search_fields = ['name', 'page_title', 'page_description', 'page_keyword']
    ordering_fields = '__all__'
    ordering = ['ID_GB_STNG']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GlobalSettingSerializer
        return GlobalSettingListSerializer

    @swagger_auto_schema(tags=['Global Settings'], operation_description="Add global setting", operation_summary="Global setting add")
    def post(self, request, *args, **kwargs):
        '''global setting create'''
        logger.info("Global setting create, User : %s ,Post Data : %s ",
                    request.user, request.data)
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {"status": "Status", "name": "Global Setting Name", "createddate": "Created Date & Time",
                                    "b_unit_assigned": "Assign To", "updatedby": "Modified By"}
        response.data['column_type'] = {"status": "status", "name": "str", "createddate": "Datetime",
                                        "b_unit_assigned": "str", "updatedby": "str"}

        return response

    @swagger_auto_schema(tags=['Global Settings'], operation_description="get global setting list", operation_summary="Global setting list")
    def get(self, request, *args, **kwargs):
        '''global setting list'''
        gb_set_id = request.GET.get('ID_GB_STNG')
        logger.info("Global Setting Id : %s", gb_set_id)
        if gb_set_id is None:
            logger.info("Global Setting ID None")
            return self.list(request, *args, **kwargs)
        else:
            logger.info("Global Setting ID  Not None")
            queryset = GlobalSetting.objects.get(ID_GB_STNG=gb_set_id)
            response_data = GlobalSettingRetrieveSerializer(queryset)
            return Response(response_data.data)


gsetting_delete_response_schema_dict = {
    "204": openapi.Response(
        description="object is deleted ,No Content in response",
    ),
    "404": openapi.Response(
        description="Not Found"
    )
}
gsetting_params = [
    openapi.Parameter("gsettingId",
                      openapi.IN_PATH,
                      description="Global setting id",
                      type=openapi.TYPE_INTEGER
                      )
]


class GlobalSettingRetrieveUpdate(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    '''global setting retrive update'''
    serializer_class = GlobalSettingUpdateSerializer
    lookup_url_kwarg = "gsettingId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gsetting_id = self.kwargs.get(self.lookup_url_kwarg)
        query = GlobalSetting.objects.filter(
            ID_GB_STNG=gsetting_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        obj = get_object_or_404(queryset, **filter)
        return obj

    @swagger_auto_schema(tags=['Global Settings'], manual_parameters=gsetting_params, operation_description="Global setting retrive", operation_summary="Global setting retrive single object")
    def get(self, request, *args, **kwargs):
        '''global setting retrive'''
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Global Settings'], manual_parameters=gsetting_params, operation_description="update global setting", operation_summary="Global setting update")
    def put(self, request, *args, **kwargs):
        '''global setting update'''
        logger.info("Global setting Update, ID : %s ,User : %s ,Post Data : %s ",
                    self.kwargs.get(self.lookup_url_kwarg), request.user, request.data)
        return self.update(request, *args, **kwargs)


class GlobalSettingPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field in serializer which is to be modified.
    '''
    serializer_class = GlobalSettingstatusSerializer
    lookup_url_kwarg = "gsettingId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gsetting_id = self.kwargs.get(self.lookup_url_kwarg)
        query = GlobalSetting.objects.filter(
            ID_GB_STNG=gsetting_id)
        return query

    @swagger_auto_schema(tags=['Global Settings'], manual_parameters=gsetting_params, operation_description="status update global setting", operation_summary="Global setting status update")
    def patch(self, request, *args, **kwargs):
        '''global setting partial update'''
        logger.info("Global setting Status Update, ID : %s ,User : %s ,Post Data : %s ",
                    self.kwargs.get(self.lookup_url_kwarg), request.user, request.data)
        return self.partial_update(request, *args, **kwargs)


class GlobalSettingstatusUpdateMultipleView(APIView):
    '''global setting multiple status update'''

    def validate_ids(self, id_list):
        '''global setting validate id'''
        for each_id in id_list:
            try:
                GlobalSetting.objects.get(ID_GB_STNG=each_id)
            except (GlobalSetting.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Global Settings'], operation_description="multiple status update global setting",
                         operation_summary="Global setting multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Global setting Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='global setting status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''global setting multiple status update'''
        id_list = request.data['ids']
        status_val = request.data['status']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            instances = []
            for each_id in id_list:
                obj = GlobalSetting.objects.get(ID_GB_STNG=each_id)
                obj.status = status_val
                obj.save()
                instances.append(obj)
            serializer = GlobalSettingstatusSerializer(instances, many=True)
            return Response(serializer.data)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GlobalSettingDeleteMultipleView(APIView):
    '''global setting multiple delete'''

    def validate_ids(self, id_list):
        '''global setting validate id'''
        for each_id in id_list:
            try:
                GlobalSetting.objects.get(ID_GB_STNG=each_id)
            except (GlobalSetting.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Global Settings'], operation_description="multiple delete global setting", operation_summary="Global setting multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Global setting Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''global setting multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                GlobalSetting.objects.filter(ID_GB_STNG=each_id).delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
