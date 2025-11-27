from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exemplo: apenas leitura de usuários (admin/painel interno)
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
