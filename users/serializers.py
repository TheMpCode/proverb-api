from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """SERIALIZER POUR L'INSCRIPTION DES UTILISATEURS"""

    class Meta:
        model = User
        fields = ["username", "email", "avatar"]
        extra_kwargs = {
            "email": {"required": True},
        }


    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            avatar=validated_data.get("avatar", ""),
            password=None
        )
        user.set_unusable_password() # PAS DE MOT DE PASSE POUR SE CONNECTER
        user.save()
        return user
    


class PasswordlessLoginSerializer(serializers.Serializer):
    """SERIALIZER POUR LA CONNEXION SANS MOT DE PASSE AVEC UN CODE OTP"""
    email = serializers.EmailField()