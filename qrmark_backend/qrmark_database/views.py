from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken

from .serializers import *

class StudentLoginAPI(generics.GenericAPIView):
    serializer_class = StudentLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        message = ""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            _, token = AuthToken.objects.create(user)
            response_data = {
                "message" : "Login successful",
                "data" : UserSerializer(user, context=self.get_serializer_context()).data,
                "token" : token
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            for field in list(e.detail):
                message = e.detail[field][0]
                response_data = {
                    "message" : message,
                    "data" : None,
                    "token" : None                 
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)