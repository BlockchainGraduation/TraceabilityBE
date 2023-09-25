from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = user.username
        # ...

        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','username', 'email', 'password','phone']
        extra_kwargs = {
            'username': {'required': True},
            'phone': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True,'required': True},
        }
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['user_permissions','groups','password']
        # fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
