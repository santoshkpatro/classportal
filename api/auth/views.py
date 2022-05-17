from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(data={'message': 'Invalid input details'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(**serializer.data)

    if not user:
        return Response(data={'message': 'Either email or password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)

    return Response(data={'access_token': str(access_token), 'refresh_token': str(refresh_token)}, status=status.HTTP_200_OK)

