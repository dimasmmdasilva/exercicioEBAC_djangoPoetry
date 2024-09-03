from rest_framework import viewsets
from ..models import Author
from ..serializers import AuthorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]