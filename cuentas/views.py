from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .serializers import UsuarioSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_anonymous:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        elif request.user.is_staff or request.user.is_superuser:
            is_staff = request.data.get('is_staff', True)
            is_superuser = request.data.get('is_superuser', False)
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=is_staff,
                is_superuser=is_superuser
            )

        else:
            user = User.objects.create_user(
                **serializer.validated_data,
                is_staff=False,
                is_superuser=False
            )

        return Response(
            UsuarioSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
