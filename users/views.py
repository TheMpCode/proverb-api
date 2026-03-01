
########### IMPORTATIONS ############

from django.core.cache import cache # STOCKER LE CACHE POUR LES CODES OTP
from rest_framework import generics # VUES GENERIQUES POUR SIMPLIFIER LA CREATION DE VUES BASIQUES

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, PasswordlessLoginSerializer
from django.contrib.auth import get_user_model

import random # POUR GENERER UN CODE OTP ALEATOIRE

from rest_framework_simplejwt.tokens import RefreshToken # POUR GERER LES TOKENS JWT APRES LA VERIFICATION OTP

#########################################





# ==> ON RECUPERE LE MODELE USER PERSONNALISE
User = get_user_model()



class UserRegistrationViewSet(generics.CreateAPIView):
    """ CreateAPIView est une vue generique qui fournit une implementation de la methode POST pour creer un nouvel objet dans la base de données"""


    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # On permet à tout le monde de s'inscrire

    # ==> ON N'AUTORISE QUE LA METHODE POST POUR S'INSCRIRE
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Surcharge de la méthode create pour personnaliser la réponse après l'inscription"""

        response = super().create(request, *args, **kwargs) # On appelle la méthode create de la classe parente pour créer l'utilisateur
        return Response(
            {"message" : "Inscription réussie ! Vous pouvez maintenant vous connecter avec votre email"},
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

            # ==> ON STOCKE LE CODE OTP DANS REDIS
            # ==> (clé: email, valeur: code, duree: 5min(300 secondes))

            cache.set(f"opt_{email}", otp_code, timeout=300) # 300 secondes = 5 minutes

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

        # ==> ON RECUPERE L'EMAIL ET LE CODE OTP FOURNI DANS LA REQUETE
        email = request.data.get("email")
        code_recu = request.data.get("code")

        # ==> ON RECUPERE LE CODE OTP STOCKE DANS REDIS
        code_stocke = cache.get(f"opt_{email}")

        if code_stocke and code_recu == code_stocke:
            # SI CORRESPONDANCE, ON SUPPRIME LE CODE OTP DU CACHE
            cache.delete(f"opt_{email}")

            # ON RECUPERE L'UTILISATEUR AVEC L'EMAIL FOURNI OU ON LE CREE S'IL N'EXISTE PAS
            user, created = User.objects.get_or_create(email=email, defaults={"username": email.split("@")[0]}) # On utilise la partie avant @ comme username par défaut

            # ON GENERE UN TOKEN
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Bon Retour Parmis Nous !",
                "access" : str(refresh.access_token),
                "refresh" : str(refresh),
                "user" : {
                    "id" : user.id,
                    "email" : user.email,
                }
            },
                status=status.HTTP_200_OK 
            )
        
        return Response(
            {"error": "Code OTP invalide ou expiré"},
            status=status.HTTP_400_BAD_REQUEST
        )


class SecretDataView(APIView):
    """ VUE PROTEGEE QUI REQUIERT UNE AUTHENTIFICATION PAR TOKEN JWT"""

    permission_classes = [IsAuthenticated] # Seuls les utilisateurs authentifiés peuvent accéder à cette vue

    def get(self, request):
        return Response(
            {"message" : f"Bravo {request.user.email} ! Tu peux voir ce message privé car tu es authentifié avec un token JWT valide."},
            status=status.HTTP_200_OK
        )