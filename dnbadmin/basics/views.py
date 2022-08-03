'''basic modules view'''
from django.core.exceptions import ValidationError
from django.db import transaction
import logging
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from party.models import Language, LegalOrganizationType
from basics.models import DateFormat, Timezone, BusinessUnitType, ImageInformation
from basics.serializers import LanguageListSerializer, DateFormatListSerializer, TimezoneListSerializer, BusinessUnitTypeSerializer, LegalOrgTypeSerializer, ImageInfoSerializer, ImageInfoCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend


logger = logging.getLogger(__name__)


class LanguageList(ListModelMixin, GenericAPIView):
    '''language list'''
    queryset = Language.objects.all()
    serializer_class = LanguageListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_LGE', 'NM_LGE']
    ordering_fields = '__all__'
    ordering = ['ID_LGE']

    @swagger_auto_schema(tags=['Basic'], operation_description="get language list", operation_summary="Language list")
    def get(self, request, *args, **kwargs):
        '''language list'''
        return self.list(request, *args, **kwargs)


class DateFormatList(ListModelMixin, GenericAPIView):
    '''DateFormat list'''
    queryset = DateFormat.objects.all()
    serializer_class = DateFormatListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_BA_DFMT', 'name']
    ordering_fields = '__all__'
    ordering = ['ID_BA_DFMT']

    @swagger_auto_schema(tags=['Basic'], operation_description="get dateformat list", operation_summary="dateformat list")
    def get(self, request, *args, **kwargs):
        '''dateformat list'''
        return self.list(request, *args, **kwargs)


class TimezoneList(ListModelMixin, GenericAPIView):
    '''Timezone list'''
    queryset = Timezone.objects.all()
    serializer_class = TimezoneListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_BA_TZN', 'timezone', 'code']
    ordering_fields = '__all__'
    ordering = ['ID_BA_TZN']

    @swagger_auto_schema(tags=['Basic'], operation_description="get timezone list", operation_summary="timezone list")
    def get(self, request, *args, **kwargs):
        '''timezone list'''
        return self.list(request, *args, **kwargs)


class BusinessUnitTypeCreateViews(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''Business Unit Type Get and Create Views Class '''
    # queryset = BusinessUnitType.objects.all()
    serializer_class = BusinessUnitTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'status']
    search_fields = ['status', 'name']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        query = BusinessUnitType.objects.all()
        return query

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {"status": "Status", "name": "Business Unit Type",
                                    "createddate": "Created Date & Time"}
        response.data['column_type'] = {
            "status": "status", "name": "str", "createddate": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Business Unit Type'], operation_description="Business unit type list", operation_summary="Business Unit Type List")
    def get(self, request, *args, **kwargs):
        ''' business unit type list '''
        bu_typ_id = request.GET.get('id')
        if bu_typ_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = BusinessUnitType.objects.get(id=bu_typ_id)
            response_data = BusinessUnitTypeSerializer(queryset)
            return Response(response_data.data)

    @swagger_auto_schema(tags=['Business Unit Type'], operation_description="Business unit type create", operation_summary="Business Unit Type Create")
    def post(self, request, *args, **kwargs):
        ''' business unit type create '''
        current_user = request.user
        request.data['createdby'] = current_user.id
        return self.create(request, *args, **kwargs)


bu_params = [
    openapi.Parameter("butypId",
                      openapi.IN_PATH,
                      description="business unit type id",
                      type=openapi.TYPE_INTEGER
                      )
]


class BusinessUnitTypeUpdateViews(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    '''Business Unit Type Views Class '''
    serializer_class = BusinessUnitTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "butypId"

    def get_queryset(self):
        butyp_id = self.kwargs.get(self.lookup_url_kwarg)
        query = BusinessUnitType.objects.filter(
            id=butyp_id)
        return query

    @swagger_auto_schema(tags=['Business Unit Type'], manual_parameters=bu_params, operation_description="Update business unit type", operation_summary="Business unit type update")
    def put(self, request, *args, **kwargs):
        '''business unit type update'''
        current_user = request.user
        request.data['updatedby'] = current_user.id
        return self.update(request, *args, **kwargs)


class BusinessUnitTypeMultipleStatusUpdate(APIView):
    '''Business unit type  multiple status update and delete'''
    permission_classes = (IsAuthenticated,)

    def validate_ids(self, id_list):
        ''' validate business unit type id'''
        for bu_unit_id in id_list:
            try:
                BusinessUnitType.objects.get(id=bu_unit_id)
            except (BusinessUnitType.DoesNotExist, ValidationError):
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

    @swagger_auto_schema(tags=['Business Unit Type'], operation_description="Business unit type multiple status update",
                         operation_summary="Business unit type multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids',
                                  items=openapi.Items(type=openapi.TYPE_INTEGER, description='Business unit type Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Business unit type status (A/I)'),
        }, required=['ids', 'status']
    ), responses=multiple_update_response_schema)
    def put(self, request):
        '''Business unit type multiple status update'''
        bu_typ_id_list = request.data['ids']
        bu_typ_status = request.data['status']
        chk_stat = self.validate_ids(id_list=bu_typ_id_list)
        current_user = request.user
        updatedby = current_user.id
        if chk_stat:
            instances = []
            for bu_typ_id in bu_typ_id_list:
                obj = BusinessUnitType.objects.get(id=bu_typ_id)
                obj.status = bu_typ_status
                obj.updatedby = updatedby
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

    @swagger_auto_schema(tags=['Business Unit Type'], operation_description="Business unit type multiple delete", operation_summary="Business unit type multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids', items=openapi.Items(type=openapi.TYPE_INTEGER, description='Business unit type Id list')),
        }, required=['ids']
    ))
    def delete(self, request):
        '''Business unit type multiple status update'''
        bu_typ_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=bu_typ_list)
        response = {}
        if chk_stat:
            for bu_typ_id in bu_typ_list:
                obj = BusinessUnitType.objects.get(id=bu_typ_id)
                obj.delete()
            response["message"] = "Item Successfully Deleted"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["message"] = "Invalid Unit of Measure Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


#! Legal Organization Type
class LegalOrgTypeCreateViews(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''Legal Organization Type Get and Create Views Class '''
    queryset = LegalOrganizationType.objects.all()
    serializer_class = LegalOrgTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'CD_LGL_ORGN_TYP']
    search_fields = ['CD_LGL_ORGN_TYP', 'status',
                     'DE_LGL_ORGN_TYP']
    ordering_fields = ['createddate']
    ordering = ['createddate']

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "status": "Status", "CD_LGL_ORGN_TYP": "Code", "DE_LGL_ORGN_TYP": "Description", "createddate": "Created Date & Time"}
        response.data['column_type'] = {
            "status": "status", "CD_LGL_ORGN_TYP": "str", "DE_LGL_ORGN_TYP": "str", "createddate": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Legal Organization Type'], operation_description="Legal organization type list", operation_summary="Legal Organization Type List")
    def get(self, request, *args, **kwargs):
        ''' Legal organization type list '''
        lglorg_typ_cd = request.GET.get('CD_LGL_ORGN_TYP')
        if lglorg_typ_cd is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = LegalOrganizationType.objects.get(
                CD_LGL_ORGN_TYP=lglorg_typ_cd)
            response_data = LegalOrgTypeSerializer(queryset)
            return Response(response_data.data)

    @swagger_auto_schema(tags=['Legal Organization Type'], operation_description="Legal organization type create", operation_summary="Legal Organization Type Create")
    def post(self, request, *args, **kwargs):
        ''' Legal organization type create '''
        current_user = request.user
        request.data['createdby'] = current_user.id
        return self.create(request, *args, **kwargs)


legal_params = [
    openapi.Parameter("legalorgtypCd",
                      openapi.IN_PATH,
                      description="Legal organization type code",
                      type=openapi.TYPE_STRING
                      )
]


class LegalOrgTypeUpdateViews(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    '''Legal Organization Type Views Class '''
    serializer_class = LegalOrgTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "legalorgtypCd"

    def get_queryset(self):
        legalorgtyp_code = self.kwargs.get(self.lookup_url_kwarg)
        query = LegalOrganizationType.objects.filter(
            CD_LGL_ORGN_TYP=legalorgtyp_code)
        return query

    @swagger_auto_schema(tags=['Legal Organization Type'], manual_parameters=legal_params, operation_description="Update legal organization type", operation_summary="Legal organization type update")
    def put(self, request, *args, **kwargs):
        '''Legal organization type update'''
        current_user = request.user
        request.data['updatedby'] = current_user.id
        return self.update(request, *args, **kwargs)


class LegalOrgTypeMultipleStatusUpdate(APIView):
    '''Legal organization type multiple status update and delete'''
    permission_classes = (IsAuthenticated,)

    def validate_ids(self, cd_list):
        ''' validate legal organization type code '''
        for legal_org_typ_cd in cd_list:
            try:
                LegalOrganizationType.objects.get(
                    CD_LGL_ORGN_TYP=legal_org_typ_cd)
            except (LegalOrganizationType.DoesNotExist, ValidationError):
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

    @swagger_auto_schema(tags=['Legal Organization Type'], operation_description="Legal organization type multiple status update",
                         operation_summary="Legal organization type multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'legal_org_type_code': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of legal org type code',
                                                  items=openapi.Items(type=openapi.TYPE_STRING, description='Legal org type code')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Legal org type status (A/I)'),
        }, required=['legal_org_type_code', 'status']
    ), responses=multiple_update_response_schema)
    def put(self, request):
        '''Legal organization type multiple status update'''
        legal_org_typ_list = request.data['legal_org_type_code']
        legal_org_typ_status = request.data['status']
        chk_stat = self.validate_ids(cd_list=legal_org_typ_list)
        current_user = request.user
        updatedby = current_user.id
        if chk_stat:
            instances = []
            for legal_org_typ_code in legal_org_typ_list:
                obj = LegalOrganizationType.objects.get(
                    CD_LGL_ORGN_TYP=legal_org_typ_code)
                obj.status = legal_org_typ_status
                obj.updatedby = updatedby
                obj.save()
                instances.append(obj)
            response = {}
            response["message"] = "Status Successfully Updated"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {}
            response["message"] = "Invalid Data"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    multiple_delete_response_schema = {
        "200": openapi.Response(
            description="Item Successfully Deleted",
        ),
        "400": openapi.Response(
            description="Bad Request"
        )
    }

    @swagger_auto_schema(tags=['Legal Organization Type'], operation_description="Legal organization type multiple delete", operation_summary="Legal organization type multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'legal_org_type_code': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Legal organization type code list')),
        }, required=['ids']
    ))
    def delete(self, request):
        '''Legal organization type multiple status update'''
        legal_org_typ_list = request.data['legal_org_type_code']
        chk_stat = self.validate_ids(cd_list=legal_org_typ_list)
        response = {}
        if chk_stat:
            for legal_org_typ_code in legal_org_typ_list:
                obj = LegalOrganizationType.objects.get(
                    CD_LGL_ORGN_TYP=legal_org_typ_code)
                obj.delete()
            response["message"] = "Item Successfully Deleted"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["message"] = "Invalid Data"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateListMixin:
    """Allows bulk creation of a resource."""

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)


response_schema = {
    "201": openapi.Response(
        description="Created Successfully",
    ),
    "400": openapi.Response(
        description="Bad Request"
    )
}


class ImageInfoCreateViews(CreateListMixin, ListModelMixin, GenericAPIView):
    ''' Image Info Create View Class '''
    queryset = ImageInformation.objects.all()
    serializer_class = ImageInfoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['imageinformation_id', 'status']
    search_fields = ['title', 'imagename',
                     'imageurl', 'image_type']
    ordering_fields = ['createddate']
    ordering = ['createddate']

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "status": "Status",
            "imagename": "Name",
            "imageurl": "Image URL",
            "acquire_license_page": "Acquire License Page",
            "alt": "Alt Tag",
            "createddate": "Created Date",
            "imageinformation_id": "Id",
            "image_license": "License",
            "modulename": "Location",
            "og_image_tag": "OG Image Tag",
            "updateddate": "Updated Date"}
        response.data['column_type'] = {
            "status": "status",
            "imagename": "str",
            "imageurl": "str",
            "acquirelicensepage": "str",
            "alt": "str",
            "createddate": "Datetime",
            "imageinformation_id": "int",
            "image_license": "str",
            "modulename": "str",
            "og_image_tag": "str",
            "updateddate": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Image Library'], operation_description="Image info list", operation_summary="Image info List")
    def get(self, request, *args, **kwargs):
        ''' Image Info list '''
        imageinfo_id = request.GET.get('imageinformation_id')
        if imageinfo_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = ImageInformation.objects.get(
                imageinformation_id=imageinfo_id)
            response_data = ImageInfoSerializer(queryset)
            return Response(response_data.data)

    @swagger_auto_schema(tags=['Image Library'], request_body=ImageInfoSerializer(many=True), operation_description="Image info store", operation_summary="Image Information Create", responses=response_schema)
    def post(self, request, *args, **kwargs):
        ''' Image Info create '''
        logger.info("Request Data : %s", request.data)
        response = {}
        try:
            with transaction.atomic():
                current_user = request.user
                logger.info("Current User : %s", current_user)
                for d in request.data:
                    d['createdby'] = current_user.id
                serializer = ImageInfoCreateSerializer(
                    data=request.data, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    http_status = status.HTTP_201_CREATED
                    message = "Created Successfully"
                    response['message'] = message
                else:
                    logger.info("Not Valid")
                    http_status = status.HTTP_400_BAD_REQUEST
                    message = "Invalid Data"
                    response['message'] = message
                return Response(response, status=http_status)
        except Exception as exp:
            logger.exception(exp)
            response = {}
            response['message'] = "Error Encountered"
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


image_params = [
    openapi.Parameter("imageinfoId",
                      openapi.IN_PATH,
                      description="Legal organization type code",
                      type=openapi.TYPE_STRING
                      )
]


class ImageInfoUpdateViews(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    '''Image Info Update Views Class '''
    serializer_class = ImageInfoSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "imageinfoId"

    def get_queryset(self):
        imageinfo_id = self.kwargs.get(self.lookup_url_kwarg)
        query = ImageInformation.objects.filter(
            imageinformation_id=imageinfo_id)
        return query

    @swagger_auto_schema(tags=['Image Library'], manual_parameters=image_params, operation_description="Update Image Library", operation_summary="Image Library update")
    def put(self, request, *args, **kwargs):
        '''Image Library update'''
        current_user = request.user
        request.data['updatedby'] = current_user.id
        return self.update(request, *args, **kwargs)


class ImageOnfoMultipleStatusUpdate(APIView):
    '''Image Info multiple status update and delete'''
    permission_classes = (IsAuthenticated,)

    def validate_ids(self, id_list):
        ''' validate Image Info Ids '''
        for iamge_id in id_list:
            try:
                ImageInformation.objects.get(
                    imageinformation_id=iamge_id)
            except (ImageInformation.DoesNotExist, ValidationError):
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

    @swagger_auto_schema(tags=['Image Library'], operation_description="Image Library multiple status update",
                         operation_summary="Image Library multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of image info id',
                                  items=openapi.Items(type=openapi.TYPE_INTEGER, description='Image info id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Image info status (A/I)'),
        }, required=['ids', 'status']
    ), responses=multiple_update_response_schema)
    def put(self, request):
        '''Image Info multiple status update'''
        image_id_list = request.data['ids']
        image_status = request.data['status']
        chk_stat = self.validate_ids(id_list=image_id_list)
        current_user = request.user
        updatedby = current_user.id
        if chk_stat:
            instances = []
            for image_id in image_id_list:
                obj = ImageInformation.objects.get(
                    imageinformation_id=image_id)
                obj.status = image_status
                obj.updatedby = updatedby
                obj.save()
                instances.append(obj)
            response = {}
            response["message"] = "Status Successfully Updated"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {}
            response["message"] = "Invalid Data"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    multiple_delete_response_schema = {
        "200": openapi.Response(
            description="Item Successfully Deleted",
        ),
        "400": openapi.Response(
            description="Bad Request"
        )
    }

    @swagger_auto_schema(tags=['Image Library'], operation_description="Image Library multiple delete", operation_summary="Image Library multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids', items=openapi.Items(type=openapi.TYPE_INTEGER, description='Image Library id list')),
        }, required=['ids']
    ))
    def delete(self, request):
        '''Image Library multiple status update'''
        image_id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=image_id_list)
        response = {}
        if chk_stat:
            for image_id in image_id_list:
                obj = ImageInformation.objects.get(
                    imageinformation_id=image_id)
                obj.delete()
            response["message"] = "Item Successfully Deleted"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["message"] = "Invalid Data"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
