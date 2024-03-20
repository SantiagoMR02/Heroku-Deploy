from django.db import models
from servicios.models import OrderJob
from inventario.models import Inventory, Input, Machine
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

DEFAULT_STA_STATES = [
    ('Realizada', 'Realizada'),
    ('En proceso', 'En proceso'),
    ('Pendiente', 'Pendiente'),
]
class StateAc (models.Model):
    stateAc = models.CharField(max_length=200,verbose_name="Estado de las Actividades", choices=DEFAULT_STA_STATES)

    def __str__(self):
        return self.stateAc
    
    class Meta: 
        verbose_name="EstadoAc"
        verbose_name_plural="EstadosAc"
        db_table="estadosac"
        ordering=['id']
        
# Lista de opciones para el campo stateN
DEFAULT_NOVELTY_STATES = [
    ('Manchado', 'Manchado'),
    ('Roto', 'Roto'),
    ('Quemado', 'Quemado'),
    ('Decolorado', 'Decolorado'),
    ('Ninguno', 'Ninguno'),
]

class Novelty(models.Model):
    dateN = models.DateField(verbose_name="Fecha de la Novedad")
    stateN = models.CharField(max_length=50, verbose_name="Estado Novedad", choices=DEFAULT_NOVELTY_STATES)
    
    def __str__(self):
        return f"{self.stateN}"
    
    class Meta:
        verbose_name = "Novedad"
        verbose_name_plural = "Novedades"
        db_table = "novedad"
        ordering = ['id']

def  no_past_dates_validators(value):
    if value<timezone.now().date():
        raise ValidationError('No se pueden ingresar fechas pasadas')

def no_negative_values_validator(value):
    if value <= 0:
        raise ValidationError("La cantidad no puede ser negativa.")



class Activity (models.Model):
    dateAc = models.DateField(verbose_name="Fecha Actividad", validators=[no_past_dates_validators])
    timeAc = models.TimeField(verbose_name="Tiempo de desarrollo actividad", blank=False, null=True)
    descriptionAc = models.TextField(verbose_name="Descripción Actividad")
    noveltyAc = models.ForeignKey(Novelty,on_delete=models.CASCADE, verbose_name="Novedad de la Actividad")
    stateAc= models.ForeignKey(StateAc,on_delete=models.CASCADE, verbose_name="Estado de Actividad")
    orderJob= models.ForeignKey('servicios.OrderJob',on_delete=models.CASCADE,verbose_name="orden de trabajo")
    input= models.ForeignKey('inventario.Input',on_delete=models.CASCADE,verbose_name="Insumo") 
    amountToUse = models.IntegerField(verbose_name="Cantidad de Insumo a utilizar" , blank=False, null=True, validators=[no_negative_values_validator])
    machine= models.ForeignKey('inventario.Machine',on_delete=models.CASCADE,verbose_name="Maquina")  
    ActivityValue= models.FloatField(verbose_name="Valor actividad")

    def save(self, *args, **kwargs):
        if self.input and self.amountToUse:
            self.input.amountI -= self.amountToUse  # Restar la cantidad a utilizar del insumo
            self.input.save()  # Guardar el insumo actualizado
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"Actividad N° {self.id}"
    
    def clean(self):
        super().clean()
        if self.input and self.amountToUse:
            if self.amountToUse > self.input.amountI:
                raise ValidationError("No hay suficientes insumos disponibles o nos quedamos sin este insumo.")
    
    class Meta: 
        verbose_name="Actividad"
        verbose_name_plural="Actividades"
        db_table="actividades"
        ordering=['id']



