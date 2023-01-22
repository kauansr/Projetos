from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserViewset(viewsets.ModelViewSet):


    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer