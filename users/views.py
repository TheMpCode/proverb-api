
from django.core.cache import cache
from rest_framework import generics

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, PasswordlessLoginSerializer
from django.contrib.auth import get_user_model

import random # POUR GENERER UN CODE OTP ALEATOIRE


# ==> ON RECUPERE LE MODELE USER PERSONNALISE
User = get_user_model()



class UserRegistrationViewSet(viewsets.ModelViewSet):
    """ViewSet pour l'inscription des utilisateurs"""

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # On permet à tout le monde de s'inscrire

    # ==> ON N'AUTORISE QUE LA METHODE POST POUR S'INSCRIRE
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Surcharge de la méthode create pour personnaliser la réponse après l'inscription"""

        # ==> ON VALIDE LES DONNEES ENTRANTES AVEC LE SERIALIZER
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ==> ON UTILISE LA METHODE PERFORM_CREATE POUR CREER L'UTILISATEUR AVEC LES DONNEES VALIDEES
        self.perform_create(serializer)

        return Response(
            {
                "message" : "Utilisateur crée avec succès"
            },
            status=status.HTTP_201_CREATED
        )
    

class RequestOTPView(APIView):
    """ VUE POUR DEMANDER UN CODE OTP POUR SE CONNECTER
        ==> ON VERFIE D'ABORD SI L'UTILISATEUR EXISTE AVEC L'EMAIL FOURNI"""
    
    def post(self, request):
        """ ON RECUPERE L'EMAIL DE LA REQUETE ET ON VERIFIE SI UN UTILISATEUR EXISTE AVEC CET EMAIL"""

        # ==> ON UTILISE LE SERIALIZER POUR VALIDER L'EMAIL FOURNI DANS LA REQUETE
        serialiser = PasswordlessLoginSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        email = serialiser.validated_data["email"]

        # ==> ON VERIFIE SI UN UTILISATEUR EXISTE AVEC CET EMAIL
        try:
            user  = User.objects.get(email=email) # On essaie de recuperer l'utilisateur avec l'email fourni

            otp_code = str(random.randint(100000, 999999)) # On genere un code OTP aleatoire a 6 chiffres

            # SIMULATION D'ENVOI
            print(f"Code OTP à {email}")
            print(f"Votre code OTP est : {otp_code}")

            return Response(
                {"message" : "Un code OTP a été envoyé à votre adresse email"},
                status=status.HTTP_200_OK
            )
        
        except User.DoesNotExist:
            return Response(
                {"error" : "Aucun utilisateur trouvé avec cet email"},
                status=status.HTTP_404_NOT_FOUND
            )




class VerifyOTPView(APIView):
    """ VUE DE VERIFCATION DU CODE OTP ENVOYE"""

    def post(self, request):

        email = request.data.get("email")
        code = request.data.get("code")

        if code:
            return Response(
                {"message" : "Bon retour parmis nous !",
                 "email" : email
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error" : "Code OTP invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )