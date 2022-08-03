from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from party.serializers import ContactPurposeTypeSerializer,ContactMethodTypeSerializer,ISO3166_1CountrySerializer,ISO3166_2CountrySubdivisionSerializer
from party.models import ContactPurposeType,ContactMethodType,ISO3166_1Country,ISO3166_2CountrySubdivision
from party.documents import ContactPurposeTypeDocument,ContactMethodTypeDocument,ISO3166_1CountryDocument,ISO3166_2CountrySubdivisionDocument
from django.db.models import Q,F
# Create your views here.

CntPrpsTypeList_response_schema_dict = {
    "200": openapi.Response(
        description="Return Contact Purpose Type List",
        examples={
            "application/json": {
                "total": "total list count",
                "contactpurposetype_list": [
                    {
                        "code": "Contact Purpose Type Code",
                        "name": "Name for the code denoting a reason"
                    }
                ]
            }
        }
    )
}
class ContactPurposeTypeList(APIView):    
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    @swagger_auto_schema(tags=['Employee Contact'],operation_description="Employee Contact Purpose List", operation_summary="Contact Purpose Type",responses=CntPrpsTypeList_response_schema_dict)
    def get(self, request):
        try:
            response=ContactPurposeTypeDocument.search().filter().execute()
            result=response.to_dict()['hits']
            data = []
            for line in result['hits']:
                data.append(line['_source'])
            response = {'total':result['total']['value'],'contactpurposetype_list': data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

CntMthdTypeList_response_schema_dict = {
    "200": openapi.Response(
        description="Return Contact Method List",
        examples={
            "application/json": {
                "total": "total list count",
                "contactmethodtype_list": [
                    {
                        "code": "Contact Method Type Code",
                        "name": "Name for the code denoting a Type"
                    }
                ]
            }
        }
    )
}
class ContactMethodTypeList(APIView):    
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    @swagger_auto_schema(tags=['Employee Contact'],operation_description="Employee Contact Method List", operation_summary="Contact Method Type",responses=CntMthdTypeList_response_schema_dict)
    def get(self, request):
        try:
            response=ContactMethodTypeDocument.search().filter().execute()
            result=response.to_dict()['hits']
            data = []
            for line in result['hits']:
                data.append(line['_source'])
            response = {'total':result['total']['value'],'contactmethodtype_list': data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

CountryList_response_schema_dict = {
    "200": openapi.Response(
        description="Return Country List",
        examples={
            "application/json": {
                "total": "total list count",
                "country_list": [
                    {
                        "code": "ISO Country Code",
                        "name": "Country Name"
                    }
                ]
            }
        }
    )
}
class CountryList(APIView):    
    permission_classes = (AllowAny,)
    authentication_class = JWTAuthentication
    @swagger_auto_schema(tags=['Employee Contact'],operation_description="Employee Contact Country List", operation_summary="Country List",responses=CountryList_response_schema_dict)
    def get(self, request):
        try:
            response=ISO3166_1CountryDocument.search().filter().execute()
            result=response.to_dict()['hits']
            data = []
            for line in result['hits']:
                data.append(line['_source'])
            response = {'total':result['total']['value'],'country_list': data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

StateList_response_schema_dict = {
    "200": openapi.Response(
        description="Return State List",
        examples={
            "application/json": {
                "total": "total list count",
                "state_list": [
                    {
                        "id": "State Id",
                        "name": "State Name",
                        "country": {                            
                            "code": "ISO Country Code",
                            "name": "Country Name"
                        }
                    }
                ]
            }
        }
    )
}
class StateList(APIView):    
    permission_classes = (AllowAny,)
    authentication_class = JWTAuthentication
    @swagger_auto_schema(tags=['Employee Contact'],operation_description="Employee Contact State List", operation_summary="State List", responses=StateList_response_schema_dict ,manual_parameters=[
            openapi.Parameter(
                "countrycode",
                openapi.IN_QUERY,
                description="Country Code",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ])
    def get(self, request):
        request = self.request
        countrycode  =request.query_params.get('countrycode', '')
        print(countrycode)
        try:
            if countrycode:                
                response=ISO3166_2CountrySubdivisionDocument.search().filter('match', **{'country.code': countrycode}).execute()
            else:                
                response=ISO3166_2CountrySubdivisionDocument.search().filter().execute()
            result=response.to_dict()['hits']
            data = []
            for line in result['hits']:
                data.append(line['_source'])
            response = {'total':result['total']['value'],'state_list': data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class TestClass(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication

    party_get_response_schema = {
    "200": openapi.Response(
        description="Get All The Party List",
        examples={
            "application/json": {
                "status" : "200"
            }
        }
    )
}

    @swagger_auto_schema(tags=['Employee'], operation_description="Party GET Test", operation_summary = "Party Get", responses=party_get_response_schema)
    def get(self, request):
        return Response({"status": status.HTTP_200_OK})

    party_create_response_schema = {
    "200": openapi.Response(
        description="Party Created Successfully",
        examples={
            "application/json": {
                "message" : "Created Successfully"
            }
        }
    ),
    "400": openapi.Response(
        description="Invalid Data",
    )
}
    
    @swagger_auto_schema(tags=['Employee'], operation_description="Party POST Test", operation_summary = "Party Create", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING)
        },
    ), responses={status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
           'message': openapi.Schema(
              type=openapi.TYPE_STRING
           )
        }
    )
    })
    def post(self, request):
        return Response({"message": "Created Successfully"},
                        status=status.HTTP_200_OK
                        )
