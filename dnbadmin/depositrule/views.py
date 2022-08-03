'''Deposit rule View'''
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    generics,
    mixins,
    views,
    permissions,
    status
)
from rest_framework import filters
from rest_framework.response import Response
from .serializers import DepositRule, DepositRuleSerializer, DepositRulestatusSerializer

deposit_rule_response_schema_dict = {
    "200": DepositRuleSerializer,
    "401": openapi.Response(
        description="Data not found"
    )
}


class DepositRuleListCreate(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    '''Deposit Rule Create API'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepositRuleSerializer
    queryset = DepositRule.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ID_RU_DS', 'SC_RU_DS']
    search_fields = ['LU_UOM_DS_PD', 'SC_RU_DS']
    ordering_fields = '__all__'
    ordering = ['ID_RU_DS']

    @swagger_auto_schema(tags=['Deposit Rule'], operation_description="Deposit Rule Create", operation_summary="Deposit Rule Create", responses=deposit_rule_response_schema_dict)
    def post(self, request):
        '''post methid called'''
        return self.create(request)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['columns'] = {
            "SC_RU_DS": "Status", "MO_DS": "Deposit Amount", "LU_UOM_DS_PD": "Unit of Measure Code", "MO_UOM_DS_PD": "Unit of Measure Amount"}
        response.data['column_type'] = {
            "SC_RU_DS": "status", "MO_DS": "price", "LU_UOM_DS_PD": "str", "MO_UOM_DS_PD": "price"}

        return response

    @swagger_auto_schema(tags=['Deposit Rule'], operation_description="Deposit Rule List", operation_summary="Deposit Rule List", responses=deposit_rule_response_schema_dict)
    def get(self, request):
        '''mixin list method called'''
        deposit_rule_id = request.GET.get('ID_RU_DS')
        if deposit_rule_id is None:
            return self.list(request)
        else:
            queryset = DepositRule.objects.get(
                ID_RU_DS=deposit_rule_id)
            response_data = DepositRuleSerializer(queryset)
            return Response(response_data.data)


class DepositRuleRetriveUpdate(generics.GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    '''Deposit Rule Detail'''
    serializer_class = DepositRuleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "depositrule_id"

    def get_queryset(self):
        '''retrive method'''
        depositrule_id = self.kwargs.get(self.lookup_url_kwarg)
        query = DepositRule.objects.filter(
            ID_RU_DS=depositrule_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    @swagger_auto_schema(tags=['Deposit Rule'], operation_description="Deposit Rule Update", operation_summary="Deposit Rule", responses=deposit_rule_response_schema_dict)
    def put(self, request, depositrule_id):
        '''update method of Deposit Rule'''
        return self.update(request)


class DepositRuleMultipleDelete(views.APIView):
    def validate_ids(self, id_list):
        '''deposit rule validate id'''
        for each_id in id_list:
            try:
                DepositRule.objects.get(ID_RU_DS=each_id)
            except (DepositRule.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Deposit Rule'], operation_description="multiple delete deposit rule", operation_summary="Deposit Rule multiple delete", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Deposit rule Id'))
        }, required=['ids']
    ))
    def delete(self, request, *args, **kwargs):
        '''deposit rule multiple delete'''
        id_list = request.data['ids']
        chk_stat = self.validate_ids(id_list=id_list)
        if chk_stat:
            for each_id in id_list:
                DepositRule.objects.filter(ID_RU_DS=each_id).delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {}
            response["message"] = "Invalid Id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DepositRulestatusUpdateMultipleView(views.APIView):
    '''deposit rule multiple status update'''

    def validate_ids(self, id_list):
        '''deposit rule validate id'''
        for each_id in id_list:
            try:
                DepositRule.objects.get(ID_RU_DS=each_id)
            except (DepositRule.DoesNotExist, ValidationError):
                return False
        return True

    @swagger_auto_schema(tags=['Deposit Rule'], operation_description="multiple status update deposit rule", operation_summary="Deposit rule multiple status update", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ids': openapi.Schema(type=openapi.TYPE_ARRAY, description='Array of Ids', items=openapi.Items(type=openapi.TYPE_STRING, description='Deposit Rule Id')),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='deposit rule status (A/I)'),
        }, required=['ids', 'status']
    ))
    def put(self, request, *args, **kwargs):
        '''deposit rule multiple status update'''
        try:
            id_list = request.data['ids']
            status_val = request.data['status']
            chk_stat = self.validate_ids(id_list=id_list)
            if chk_stat:
                instances = []
                for each_id in id_list:
                    obj = DepositRule.objects.get(ID_RU_DS=each_id)
                    obj.SC_RU_DS = status_val
                    obj.save()
                    instances.append(obj)
                serializer = DepositRulestatusSerializer(instances, many=True)
                return Response(serializer.data)
            else:
                response = {}
                response["message"] = "Invalid Id"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            response = {}
            response["message"] = "Ids must be Integer"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
