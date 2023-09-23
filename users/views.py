from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ResponseUserSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from .models import User

# Create your views here.

class RegisterView(APIView):
    permission_classes=[AllowAny]
    @swagger_auto_schema(tags=['auth'], operation_summary='User Register')
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    @swagger_auto_schema(tags=['auth'], operation_summary='User Login')
    def post(self, request, *args, **kargs):
        response = super().post(request, *args, **kargs)
        # access = response.data['access']
        response.set_cookie('access',response.data['access'],httponly=False)
        response.set_cookie('refresh',response.data['refresh'],httponly=False)
        return response

class MyTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=['auth'], operation_summary='User Logout')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags=['auth'], operation_summary='User Logout')
    def post(self,request):
        reponse=Response()
        reponse.data={"Message": "You are logged out"}
        reponse.delete_cookie('access')
        reponse.delete_cookie('refresh')
        return reponse



class UserView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        # serializer = RegisterSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        
        user=User.objects.get(id=request.user.pk)
        serializer=ResponseUserSerializer(user)
        content = {
            'user': str(request.user.pk),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(serializer.data)