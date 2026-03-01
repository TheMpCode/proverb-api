from rest_framework import serializers
from django.contrib.auth import get_user_model


# ==> ON RECUPERE LE MODELE USER PERSONNALISE
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """SERIALIZER POUR L'INSCRIPTION DES UTILISATEURS"""

    # CHAMP AVATAR OPTIONNEL
    avatar = serializers.URLField(required=False, 
                                  allow_blank=True,
                                  default="https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png")

    class Meta:
        model = User
        fields = ["username", "email", "avatar"] # CHAMPS DE L'UTILISATEUR A INSERER DANS LA BASE DE DONNEES
        extra_kwargs = {
            "email": {"required": True}, # ON REND L'EMAIL OBLIGATOIRE POUR S'INSCRIRE
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