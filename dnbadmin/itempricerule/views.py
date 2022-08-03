''' Item Price Rule View '''
from django.core.exceptions import ValidationError
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from product.models import ItemSellingPrices
from .serializers import ItemPriceRuleSerializer

# Create your views here.


class ItemPriceRuleViews(CreateModelMixin, ListModelMixin, GenericAPIView):
    '''Item Price Rule Get and Create Views Class '''
    serializer_class = ItemPriceRuleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_ITM_SL_PRC', 'ITM_SL_PRC_STATUS']
    search_fields = ['ITM_SL_PRC_STATUS', 'TY_PRC_RT', 'ITM_SL_PRC_NAME']
    ordering_fields = ['ID_ITM_SL_PRC']
    ordering = ['ID_ITM_SL_PRC']

    def get_queryset(self):
        query = ItemSellingPrices.objects.all()
        return query

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "ITM_SL_PRC_STATUS": "Status", "ITM_SL_PRC_NAME": "Item Price Rule Name", "RP_PR_SLS": "Permanent Price", "DC_PRC_EF_PRN_RT": "Permanent Price Effective Date", "RP_SLS_CRT": "Current Sale Unit Price", "DC_PRC_SLS_EF_CRT": "Current Sale Unit Price Effective Date", "RP_PRC_MF_RCM_RT": "Manu. Sale Unit Rec. Price", "DC_PRC_MF_RCM_RT": "Manu. Sale Unit Rec. Price Effective Dtae"}
        response.data['column_type'] = {
            "ITM_SL_PRC_STATUS": "status", "ITM_SL_PRC_NAME": "str", "RP_PR_SLS": "price", "DC_PRC_EF_PRN_RT": "Datetime", "RP_SLS_CRT": "price", "DC_PRC_SLS_EF_CRT": "Datetime", "RP_PRC_MF_RCM_RT": "price", "DC_PRC_MF_RCM_RT": "Datetime"}

        return response

    @swagger_auto_schema(tags=['Item Price Rule'], operation_description="Item Price Rule list", operation_summary="Item Price Rule List")
    def get(self, request, *args, **kwargs):
        ''' Item Price Rule list '''
        item_price_id = request.GET.get('ID_ITM_SL_PRC')
        if item_price_id is None:
            return self.list(request, *args, **kwargs)
        else:
            queryset = ItemSellingPrices.objects.get(
                ID_ITM_SL_PRC=item_price_id)
            response_data = ItemPriceRuleSerializer(queryset)
            return Response(response_data.data)

    @swagger_auto_schema(tags=['Item Price Rule'], operation_description="Item Price Rule create", operation_summary="Item Price Rule Create")
    def post(self, request, *args, **kwargs):
        ''' Item Price Rule create '''
        current_user = request.user
        request.data['createdby'] = current_user.id
        return self.create(request, *args, **kwargs)


item_params = [
    openapi.Parameter("itemPriceRuleID",
                      openapi.IN_PATH,
                      description="item price rule id",
                      type=openapi.TYPE_INTEGER
                      )
]


class ItemPriceRuleUpdateViews(UpdateModelMixin,  GenericAPIView):
    '''Business Unit Type Views Class '''
    serializer_class = ItemPriceRuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "itemPriceRuleID"

    def get_queryset(self):
        item_price_rule_id = self.kwargs.get(self.lookup_url_kwarg)
        query = ItemSellingPrices.objects.filter(
            ID_ITM_SL_PRC=item_price_rule_id)
        return query

    @swagger_auto_schema(tags=['Item Price Rule'], manual_parameters=item_params, operation_description="Update Item Price Rule", operation_summary="Item Price Rule update")
    def put(self, request, *args, **kwargs):
        '''Item Price Rule update'''
        current_user = request.user
        request.data['updatedby'] = current_user.id
        return self.update(request, *args, **kwargs)


class ItemPriceRuleMultipleStatusUpdate(APIView):
    '''Item Price Rule multiple status update and delete'''
    permission_classes = (IsAuthenticated,)

    def validate_ids(self, item_price_id_list):
        ''' validate Item Price Rule id'''
        for item_price_id in item_price_id_list:
            try:
                ItemSellingPrices.objects.get(ID_ITM_SL_PRC=item_price_id)
            except (ItemSellingPrices.DoesNotExist, ValidationError):
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

    @swagger_auto_schema(tags=['Item Price Rule'], operation_description="Item Price Rule multiple status update",
                         operation_summary="Item Price Rule multiple multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids',
                                  items=openapi.Items(type=openapi.TYPE_INTEGER, description='Item Price Rule Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Item Price Rule status (A/I)'),
        }, required=['ids', 'status']
    ), responses=multiple_update_response_schema)
    def put(self, request):
        '''Item Price Rule multiple status update'''
        item_price_id_list = request.data['ids']
        item_price_rule_status = request.data['status']
        chk_stat = self.validate_ids(item_price_id_list=item_price_id_list)
        current_user = request.user
        updatedby = current_user.id
        if chk_stat:
            instances = []
            for item_price_id in item_price_id_list:
                obj = ItemSellingPrices.objects.get(
                    ID_ITM_SL_PRC=item_price_id)
                obj.ITM_SL_PRC_STATUS = item_price_rule_status
                obj.updatedby = updatedby
                obj.save()
                instances.append(obj)
            response = {}
            response["message"] = "Status Successfully Updated"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {}
            response["message"] = "Item Price Rule Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    multiple_delete_response_schema = {
        "200": openapi.Response(
            description="Item Successfully Deleted",
        ),
        "400": openapi.Response(
            description="Bad Request"
        )
    }

    @swagger_auto_schema(tags=['Item Price Rule'], operation_description="Item Price Rule multiple delete", operation_summary="Item Price Rule multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Ids', items=openapi.Items(type=openapi.TYPE_INTEGER, description='Item Price Rule Id list')),
        }, required=['ids']
    ))
    def delete(self, request):
        '''Item Price Rule multiple status update'''
        item_price_id_list = request.data['ids']
        chk_stat = self.validate_ids(item_price_id_list=item_price_id_list)
        response = {}
        if chk_stat:
            for item_price_id in item_price_id_list:
                obj = ItemSellingPrices.objects.get(
                    ID_ITM_SL_PRC=item_price_id)
                obj.delete()
            response["message"] = "Item Successfully Deleted"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["message"] = "Invalid Item Price Rule Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
