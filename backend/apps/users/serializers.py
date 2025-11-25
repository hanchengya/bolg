from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'avatar', 'bio', 'location', 'website',
                  'follower_count', 'following_count', 'date_joined', 'is_staff']
        read_only_fields = ['id', 'follower_count', 'following_count', 'date_joined', 'is_staff']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'location', 'website']


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
