'''View of selling rule'''
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import (
    generics,
    views,
    permissions,
    mixins,
    status, filters
)
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ItemTenderRestrictionGroupSerializer, ItemTenderRestrictionGroup, ItemSellingRule, SellingRulestatusSerializer, SellingRuleCreateSerializer, SellingRuleRetriveSerializer, SellingRuleListSerializer


item_groupresponse_schema_dict = {
    "200": ItemTenderRestrictionGroupSerializer,
    "401": openapi.Response(
        description="No active account found with the given credentials"
    )
}


class ItemTenderRestrictionGroupListCreate(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    '''Item Tender Restriction Group Create and Get'''
    serializer_class = ItemTenderRestrictionGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ItemTenderRestrictionGroup.objects.all()
    filter_backend = [DjangoFilterBackend]
    filterset_fields = ['LU_GP_TND_RST']

    @swagger_auto_schema(tags=['ItemTenderRestrictionGroup'], operation_description="Item Tender Create", operation_summary="Item Tender Group Create", responses=item_groupresponse_schema_dict)
    def post(self, request):
        '''item tender group create method'''
        return self.create(request)

    @swagger_auto_schema(tags=['ItemTenderRestrictionGroup'], operation_description="Item Tender List", operation_summary="Item Tender Group", responses=item_groupresponse_schema_dict)
    def get(self, request):
        '''item tender group get method'''
        return self.list(request)


class ItemTenderRestrictionGroupRetriveUpdate(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    '''Item Tender Detail'''
    serializer_class = ItemTenderRestrictionGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "itemtender_id"

    def get_queryset(self):
        '''retrive method'''
        itemtender_id = self.kwargs.get(self.lookup_url_kwarg)
        query = ItemTenderRestrictionGroup.objects.filter(
            LU_GP_TND_RST=itemtender_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    @swagger_auto_schema(tags=['ItemTenderRestrictionGroup'], operation_description="Item Tender Update", operation_summary="Item Tender Group", responses=item_groupresponse_schema_dict)
    def put(self, request, itemtender_id):
        '''item tender group update method'''
        return self.update(request)

    @swagger_auto_schema(tags=['ItemTenderRestrictionGroup'], operation_description="Item Tender Update", operation_summary="Item Tender Group", responses=item_groupresponse_schema_dict)
    def patch(self, request, itemtender_id):
        '''item tender group partial update method'''
        return self.partial_update(request)

    @swagger_auto_schema(tags=['ItemTenderRestrictionGroup'], operation_description="Item Tender Delete", operation_summary="Item Tender Restriction Group", responses=item_groupresponse_schema_dict)
    def delete(self, request, itemtender_id):
        '''item tender delete method '''
        return self.destroy(request)


class ItemSellingRuleListCreate(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    '''
    Item Selling Rule API
    '''
    queryset = ItemSellingRule.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_RU_ITM_SL', 'status']
    search_fields = ['NM_RU_ITM_SL', 'DE_RU_ITM_SL']
    ordering_fields = '__all__'
    ordering = ['ID_RU_ITM_SL']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SellingRuleListSerializer
        return SellingRuleCreateSerializer

    @swagger_auto_schema(tags=['Item Selling Rule'], operation_description="Item Selling Create", operation_summary="Item Selling Create")
    def post(self, request, *args, **kwargs):
        '''Item Selling create method'''
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "status": "Status", "NM_RU_ITM_SL": "Selling Rule Name", "DE_RU_ITM_SL": "Description", "deposit_rule": "Deposit Rule",
            "QU_MNM_SLS_UN": "Minimum Sale Unit", "QU_UN_BLK_MXM": "Maximum Sale Unit", "DC_ITM_SLS":
            "Selling Status Effective Date", "expired_date": "Selling Status Expire Date"}
        response.data['column_type'] = {
            "status": "status", "NM_RU_ITM_SL": "str", "DE_RU_ITM_SL": "str", "deposit_rule": "str",  "QU_MNM_SLS_UN": "int", "QU_UN_BLK_MXM": "int",
            "DC_ITM_SLS": "Datetime", "expired_date": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Item Selling Rule'], operation_description="Item Selling List", operation_summary="Item Selling List")
    def get(self, request, *args, **kwargs):
        '''Item Selling list method'''
        selling_rule_id = request.GET.get('ID_RU_ITM_SL')
        if selling_rule_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = ItemSellingRule.objects.get(
                ID_RU_ITM_SL=selling_rule_id)
            response_data = SellingRuleRetriveSerializer(queryset)
            return Response(response_data.data)


class ItemSellingRuleRetriveUpdate(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    '''
    Item Selling Detail API
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "itemselling_id"

    def get_queryset(self):
        '''retrive method'''
        itemselling_id = self.kwargs.get(self.lookup_url_kwarg)
        query = ItemSellingRule.objects.filter(
            ID_RU_ITM_SL=itemselling_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SellingRuleRetriveSerializer
        return SellingRuleCreateSerializer

    @swagger_auto_schema(tags=['Item Selling Rule'], operation_description="Item Selling Update", operation_summary="Item Selling Update")
    def put(self, request, *args, **kwargs):
        '''item selling rule update'''
        return self.update(request, *args, **kwargs)


class SellingRuleMultipleDelete(views.APIView):
    '''selling rule multiple delete'''

    def validate_ids(self, id_list):
        '''item selling rule validate id'''
        for each_id in id_list:
            try:
                ItemSellingRule.objects.get(ID_RU_ITM_SL=each_id)
            except (ItemSellingRule.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Item Selling Rule'], operation_description="multiple delete selling rule", operation_summary="Selling Rule multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Deposit rule Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''selling rule multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                ItemSellingRule.objects.filter(ID_RU_ITM_SL=each_id).delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class SellingRulestatusUpdateMultipleView(views.APIView):
    '''selling rule multiple status update'''

    def validate_ids(self, id_list):
        '''selling rule validate id'''
        for each_id in id_list:
            try:
                ItemSellingRule.objects.get(ID_RU_ITM_SL=each_id)
            except (ItemSellingRule.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Item Selling Rule'], operation_description="multiple status update selling rule", operation_summary="Selling rule multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Deposit Rule Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='selling rule status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''selling rule multiple status update'''
        try:
            id_list = request.data['ids']
            status_val = request.data['status']
            chk_stat = self.validate_ids(id_list=id_list)
            if chk_stat:
                instances = []
                for each_id in id_list:
                    obj = ItemSellingRule.objects.get(ID_RU_ITM_SL=each_id)
                    obj.status = status_val
                    obj.save()
                    instances.append(obj)
                serializer = SellingRulestatusSerializer(instances, many=True)
                return Response(serializer.data)
            else:
                response = {}
                response["message"] = "Invalid Id"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            response = {}
            response["message"] = "Ids must be Integer"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
