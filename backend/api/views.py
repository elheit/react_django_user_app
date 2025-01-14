import random
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from api import serializers as api_serializer
from userauths.models import User, Profile
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class MyTokenObtainPairSerializerView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer

def generate_random_otp(length=7):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = User.objects.filter(email=email).first() # api/v1/password-reset/(email@)/

        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"
            # this link send to user in email

            print('==========> link %s: ',link)

            mail_data = {
                "link": link,
                "username": user.username,
            }
            subject = "Password Reset Email"
            text_body = render_to_string("email/password_reset.txt", mail_data)
            html_body = render_to_string("email/password_reset.html", mail_data)
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email="meslamineelheit@gmail.com",
                to = [user.email],
                body = text_body,
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()

        return user
    
class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer


    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uuidb64 = payload['uuidb64']
        password = payload['password']

        user  = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response({"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
    
        return Response({"message": "User Does Not exist"}, status=status.HTTP_404_NOT_FOUND)
