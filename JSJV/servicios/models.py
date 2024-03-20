from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

DEFAULT_STATES = [
    ('Manchado', 'Manchado'),
    ('Roto', 'Roto'),
    ('Quemado', 'Quemado'),
    ('Decolorado', 'Decolorado'),
    ('Ninguno', 'Ninguno'),
]

DEFAULT_CATEGORY_STATES = [
    ('Camisa', 'Camisa'),
    ('Pantalon', 'Pantalon'),
    ('Sudadera', 'Sudadera'),
    ('Chaqueta', 'Chaqueta'),
    ('Zapatos', 'Zapatos'),
    ('Traje', 'Traje'),
    ('Peluches', 'Peluches'),
    ('Alfombra', 'Alfombra'),
    ('Muebles', 'Muebles'),
    ('Sueter', 'Sueter'),
    ('Camiseta', 'Camiseta'),
]

DEFAULT_SERVICE = [
    ('Lavanderia', 'Lavanderia'),
    ('Tintoreria', 'Tintoreria'),
    ('Lavado especial', 'Lavado especial'),
]

DEFAULT_PAYMENT_STATES = [
    ('Efectivo', 'Efectivo'),
    ('Nequi', 'Nequi'),
    ('Daviplata', 'Daviplata'),
    ('Mastercard', 'Mastercard'),
    ('Visa', 'Visa'),
]

class ProductList(models.Model):
    amount = models.IntegerField(verbose_name="Cantidad Producto", blank=False, null=True)
    description = models.TextField(verbose_name="Descripcion Producto", blank=True, null=True)
    status = models.CharField(verbose_name="Estado del producto", max_length=255, choices=DEFAULT_STATES)
    category = models.CharField(verbose_name="Categoria del Producto", max_length=255, choices=DEFAULT_CATEGORY_STATES)
    
    def __str__(self):
        return f"Producto {self.category}"
    
    class Meta:
        verbose_name = "Listado de Producto"
        verbose_name_plural = "Listado de Productos"
        db_table = "listado_producto"
        ordering = ['id']

class TypeService(models.Model):
    descriptionTS = models.CharField(verbose_name="Descripcion", max_length=255, blank=True, null=True, choices=DEFAULT_SERVICE)
    value = models.FloatField(verbose_name="Valor", default=0.00)
    
    def __str__(self):
        return f" {self.descriptionTS}"

    class Meta:
        verbose_name = "Tipo de Servicio"
        verbose_name_plural = "Tipos de Servicio"
        db_table = "tipo_de_servicio"
        ordering = ['id']
        
def no_past_dates_validators(value):
    if value < timezone.now().date():
        raise ValidationError('No se pueden ingresar fechas pasadas')

class Income(models.Model):
    paymentMethod = models.TextField(verbose_name="Metodo De Pago", blank=False, null=True, choices=DEFAULT_PAYMENT_STATES)
    
    def __str__(self):
        return f"{self.paymentMethod}"

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        db_table = "ingresos"
        ordering = ['id']

class OrderJob(models.Model):
    nombre_cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_jobs_cliente', verbose_name="Nombre del Cliente", null=True, blank=False)
    email_cliente = models.EmailField(verbose_name="Correo Electrónico", blank=True, null=True, editable=False)  # Nuevo campo para el correo electrónico del cliente
    numberPhone = models.BigIntegerField(verbose_name="Numero de celular", blank=False, null=True)
    dateOT = models.DateField(verbose_name="Fecha entrada", validators=[no_past_dates_validators])
    productList = models.ForeignKey(ProductList, on_delete=models.CASCADE, related_name='order_jobs_product',verbose_name="Listado de Productos")
    typeService = models.ForeignKey(TypeService, on_delete=models.CASCADE, related_name='order_jobs_type_service', verbose_name="Tipo de Servicio")
    paymentMethod = models.ForeignKey(Income, on_delete=models.CASCADE, related_name='order_jobs_payment_method', verbose_name="Método de Pago", null=True, blank=False)
    totalPrice = models.FloatField(verbose_name="Valor Total", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calcular el valor total basado en el valor del servicio y la cantidad del producto
        if self.typeService and self.productList.amount:
            valor_servicio = self.typeService.value
            cantidad = self.productList.amount
            self.totalPrice = Decimal(valor_servicio) * cantidad
        # Obtener y almacenar el correo electrónico del cliente seleccionado
        if self.nombre_cliente:
            self.email_cliente = self.nombre_cliente.email
        super().save(*args, **kwargs)


    
    def __str__(self):
        return f"Orden de Trabajo {self.id}"

    class Meta:
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Ordenes de trabajo"
        db_table = "orden_trabajo"
        ordering = ['id']

class OutputOJ(models.Model):
    orderJob = models.ForeignKey(OrderJob, on_delete=models.CASCADE, verbose_name="Orden de Trabajo", blank=False, null=True)
    amountOutputs = models.IntegerField(verbose_name="Cantidad Salidas", blank=False, null=True)
    dateOutput = models.DateField(verbose_name="Fecha salida", blank=False, null=True, validators=[no_past_dates_validators])

    def __str__(self):
        return f"Salida OT {self.id}"

    class Meta:
        verbose_name = "Salida OT"
        verbose_name_plural = "Salidas OT"
        db_table = "salidas_ot"
        ordering = ['id']

    @property
    def is_date_valid(self):
        today = timezone.now().date()
        if self.dateOutput < today:
            raise ValidationError("La fecha no puede ser en el pasado.")
        return True

    def save(self, *args, **kwargs):
        if self.pk is None:  # Solo para nuevas instancias, para evitar que la resta se realice en actualizaciones
            product_list = self.orderJob.productList
            if product_list:
                product_list.amount -= self.amountOutputs
                product_list.save()  # Guardar la instancia de ProductList actualizada

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.amountOutputs is not None and self.orderJob is not None:
            product_list = self.orderJob.productList
            if product_list and self.amountOutputs > product_list.amount:
                raise ValidationError("La cantidad de salidas no puede ser mayor que la cantidad de productos disponibles en la lista.")
