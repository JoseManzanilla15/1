from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from inventario.models import Producto, Categoria
from inventario.serializers import ProductoSerializer, CategoriaSerializer, ProductoPostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated


class ProductoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class InventarioListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        nombre = self.request.query_params.get("nombre")
        busqueda = self.request.query_params.get("busqueda")
        categoria = self.request.query_params.get("categoria")
        data = Producto.objects.all()

        if nombre:
            data = data.filter(nombre__icontains=nombre)

        if busqueda:
            data = data.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripcion__icontains=busqueda)
            )

        if categoria:
            if categoria.isdigit():
                data = data.filter(categoria__id=categoria)
            else:
                data = data.filter(categoria__nombre__icontains=categoria)

        paginator = ProductoPagination()
        page = paginator.paginate_queryset(data, request)
        serializer = ProductoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = ProductoPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InventarioDetailView(APIView):
    def get(self, request, pk=None):
        try:
            data = Producto.objects.get(pk=pk)
            serializer = ProductoSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response(data={"message": "el producto no existe"},
                     status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk=None):
        try:
            data = Producto.objects.get(pk=pk)
            serializer = ProductoPostSerializer(data, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"producto editado"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            return Response({"message":"No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk=None):
        try:
            data = Producto.objects.get(pk=pk)
            serializer = ProductoPostSerializer(data, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"producto editado"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            return Response({"message":"No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk=None):
        try:
            data = Producto.objects.get(pk=pk)
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response({"message":"No se encontro el producto"}, status=status.HTTP_404_NOT_FOUND)

class CategoriaListView(APIView):
    def get(self, request):
        data = Categoria.objects.all()
        nombre = self.request.query_params.get("nombre")
        if nombre:
            data = data.filter(nombre__icontains=nombre)
        serializer = CategoriaSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        print(request.data)
        serializer = CategoriaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoriaDetailView(APIView):
    def get(self, request, pk=None):
        try:
            data = Categoria.objects.get(pk=pk)
            serializer = CategoriaSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response(data={"message": "la categoria no existe"},
                     status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk=None):
        try:
            data = Categoria.objects.get(pk=pk)
            serializer = CategoriaSerializer(data, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"categoria editada"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categoria.DoesNotExist:
            return Response({"message":"No se encontro la categoria"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk=None):
        try:
            data = Categoria.objects.get(pk=pk)
            serializer = CategoriaSerializer(data, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"categoria editada"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categoria.DoesNotExist:
            return Response({"message":"No se encontro la categoria"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk=None):
        try:
            data = Categoria.objects.get(pk=pk)
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Categoria.DoesNotExist:
            return Response({"message":"No se encontro la categoria"}, status=status.HTTP_404_NOT_FOUND)

