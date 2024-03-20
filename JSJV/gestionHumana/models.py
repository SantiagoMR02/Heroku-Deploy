from django.db import models
from django.contrib.auth.models import User
from actividades.models import Activity


DEFAULT_SCHEDULE = [
    ('8 Horas', '8 Horas'),
    ('5 Horas', '5 Horas'),
    ('6 Horas', '6 Horas'),
]

    
class Schedule(models.Model):
    schedule = models.CharField(verbose_name="Horario del empleado", max_length=255, choices=DEFAULT_SCHEDULE)

    def __str__(self):
        return f"{self.schedule}"

    class Meta: 
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        db_table = "horario"
        ordering = ['id']




class Salary(models.Model):
    nameEmploye = models.ForeignKey(User, on_delete=models.CASCADE, related_name='name_employe', verbose_name="Nombre del Empleado", null=True, blank=False)
    detailSalary = models.CharField(verbose_name="Detalle salario", blank=True, null=True, max_length=100)
    numberAccount = models.BigIntegerField(verbose_name="Numero de Cuenta", blank=False, null=True)
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='Activity_ActivityValue', verbose_name="Actividad")
    schedules = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name="Ingreso de Empleado")
    amountActivity = models.IntegerField(verbose_name="Cantidad de Actividad", blank=False, null=True)
    totalSalary = models.FloatField(verbose_name="Total salario", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.Activity and self.amountActivity:
            # Calcular el totalSalary multiplicando la cantidad de actividad por el valor de la actividad
            self.totalSalary = self.amountActivity * self.Activity.ActivityValue
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salario N° {self.id}"
    
    class Meta: 
        verbose_name = "Salario"
        verbose_name_plural = "Salarios"
        db_table = "sueldo"
        ordering = ['id']

