''' Login Authentication Serializer '''
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


#pylint: disable=W0223
class LoginSerializer(TokenObtainPairSerializer):
    ''' Login Serializer '''
    username = serializers.CharField(
        max_length=255, min_length=5, allow_blank=False)
    password = serializers.CharField(
        max_length=40, min_length=8, allow_blank=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['id'] = self.user.pk
        return data


class SignUpSerializer(serializers.Serializer):
    ''' Sign Up Serializer '''
    username = serializers.CharField(
        max_length=255, min_length=5, allow_blank=False)
    password = serializers.CharField(
        max_length=40, min_length=8, allow_blank=False)
    email = serializers.CharField(
        max_length=150, min_length=8, allow_blank=False)


class LogoutSerializer(serializers.Serializer):
    ''' This is a logout serializer '''
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
