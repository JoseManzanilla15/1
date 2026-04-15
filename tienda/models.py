from django.db import models
from inventario.models import BaseModel, Producto
from django.contrib.auth.models import User

class Compra(BaseModel):
    proveedor = models.CharField(max_length=150)
    total = models.DecimalField(decimal_places=2, default=0,max_digits=8)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Proveedor: {self.proveedor} Total: {self.total}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

class CompraDetalle(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(decimal_places=2, default=0.1,max_digits=8)
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "CompraDetalle"
        verbose_name_plural = "ComprasDetalle"

    def __str__(self):
        return f"Producto: {self.producto.nombre} Cantidad: {self.cantidad}"

class Venta(BaseModel):
    total = models.DecimalField(decimal_places=2, default=0,max_digits=8)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cliente: {self.cliente} Total: {self.total}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

class VentaDetalle(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(decimal_places=2, default=0.1,max_digits=8)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)

    def __str__(self):
        return f"Producto: {self.producto.nombre} Cantidad: {self.cantidad}"

    class Meta:
        verbose_name = "VentaDetalle"
        verbose_name_plural = "VentaDetalles"