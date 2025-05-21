

# users/serializers.py
from djoser.serializers import UserCreateSerializer as BaseCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from users.models import CustomUser

class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        model = CustomUser
        fields = ("id", "email", "password","re_password")
        
    def create(self, validated_data):
        user = super().create(validated_data)  # legt User an
        user.is_active = False                 # Konto deaktivieren
        user.save(update_fields=["is_active"])
        return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ("id", "email")

