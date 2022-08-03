''' User Signup, Signin '''
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from login_authentication.serializers import LoginSerializer, SignUpSerializer
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LogoutSerializer

# Create your views here.
logger = logging.getLogger(__name__)
login_response_schema_dict = {
    "200": openapi.Response(
        description="Login Successfull",
        examples={
            "application/json": {
                "access": "Access Token",
                "refresh": "Refresh Token",
                "username": "Username",
                "id": "User Id"
            }
        }
    ),
    "401": openapi.Response(
        description="Invalid Username or Password"
    )
}


class Login(TokenObtainPairView):
    ''' User Login '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Login url to get access token", operation_summary="Login",
                         request_body=LoginSerializer, responses=login_response_schema_dict)
    def post(self, request):
        ''' User Login '''
        serializer = LoginSerializer()
        login_response = {}
        http_status = None
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        logger.info("User : %s", user)
        if user:
            logger.info("Valid User")
            serializer_data = serializer.validate(attrs=request.data)
            logger.info("Serializer Data : %s ", serializer_data)
            login_response = serializer_data
            http_status = status.HTTP_200_OK
        else:
            logger.info("Invalid User")
            login_response['message'] = "Invalid Username or Password"
            http_status = status.HTTP_401_UNAUTHORIZED
        return Response(login_response, status=http_status)


logout_response_schema_dict = {
    "204": openapi.Response(
        description="Logout Successfull",
    ),
    "400": openapi.Response(
        description="Bad Request"
    )
}


class Logout(APIView):
    ''' Logout User '''
    permission_classes = (IsAuthenticated,)

    serializer_class = LogoutSerializer

    @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Logout user and blacklist refresh tokens", operation_summary="Logout",
                         request_body=LogoutSerializer, responses=logout_response_schema_dict)
    def post(self, request):
        ''' Black List Refresh Token '''

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUp(APIView):
    ''' Register User '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Register User", operation_summary="Sign Up", request_body=SignUpSerializer)
    @transaction.atomic
    def post(self, request):
        ''' Register User '''
        response = {}
        http_status = None

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            User.objects.create_user(**data)
            response["message"] = "User Created Successfully"
            http_status = status.HTTP_201_CREATED
        else:
            response["errors"] = serializer.errors
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(
            response,
            status=http_status
        )
