from rest_framework import serializers
from .models import Compra, CompraDetalle, Venta, VentaDetalle


class CompraDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraDetalle
        fields = ("cantidad", "precio", "producto")


class CompraSerializer(serializers.ModelSerializer):
    detalles = CompraDetalleSerializer(many=True, write_only=True)
    creado_por = serializers.ReadOnlyField(source="creado_por.username")

    class Meta:
        model = Compra
        fields = ("proveedor", "creado_por", "fecha_creacion",
                  "fecha_modificacion", "total", "id", "detalles")
        read_only_fields = ['total']


class VentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        fields = ("cantidad", "precio", "producto")
        read_only_fields = ['precio']


class VentaSerializer(serializers.ModelSerializer):
    detalles = VentaDetalleSerializer(many=True, write_only=True)
    cliente = serializers.ReadOnlyField(source="cliente.username")

    class Meta:
        model = Venta
        fields = ("cliente",  "fecha_creacion",
                  "fecha_modificacion", "total", "id", "detalles")
        read_only_fields = ['total']
