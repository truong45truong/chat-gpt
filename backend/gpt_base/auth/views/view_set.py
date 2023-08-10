from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from gpt_base.auth.serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from gpt_base.common.utils.exceptions import CustomerInvalidToken


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenViewBase):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise CustomerInvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
