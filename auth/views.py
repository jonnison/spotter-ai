
from django.contrib.auth.models import User
from auth.serializers import UserRegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer