'''store modules view'''
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from store.models import BusinessUnit, BusinessUnitGroup
from store.serializers import BusinessUnitListSerializer, BusinessUnitGroupListSerializer
from django_filters.rest_framework import DjangoFilterBackend


class BusinessUnitList(ListModelMixin, GenericAPIView):
    '''BusinessUnit list'''
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_BSN_UN', 'NM_BSN_UN']
    ordering_fields = '__all__'
    ordering = ['ID_BSN_UN']

    @swagger_auto_schema(tags=['Business Unit'], operation_description="get business unit list", operation_summary="BusinessUnit list")
    def get(self, request, *args, **kwargs):
        '''BusinessUnit list'''
        return self.list(request, *args, **kwargs)


class BusinessUnitGroupList(ListModelMixin, GenericAPIView):
    '''BusinessUnitGroup list'''
    queryset = BusinessUnitGroup.objects.all()
    serializer_class = BusinessUnitGroupListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ID_BSNGP', 'NM_BSNGP']
    ordering_fields = '__all__'
    ordering = ['ID_BSNGP']

    @swagger_auto_schema(tags=['Business Unit Group'], operation_description="get business unit group list", operation_summary="BusinessUnit Group list")
    def get(self, request, *args, **kwargs):
        '''BusinessUnit Group list'''
        return self.list(request, *args, **kwargs)
