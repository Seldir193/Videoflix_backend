

# users/serializers.py
from djoser.serializers import UserCreateSerializer as BaseCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from users.models import CustomUser

class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        model = CustomUser
        fields = ("id", "email", "password")

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ("id", "email")

