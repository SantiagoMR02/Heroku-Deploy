from django.db import models

class Input(models.Model):
    supplier_nameI=models.CharField(max_length=50,verbose_name="Nombre proveedor")
    amountI = models.IntegerField(verbose_name="Cantidad")
    product_type=models.CharField(max_length=20,verbose_name="Tipo insumo")
    
    
     #Metodo To String
    def __str__(self) :
        return f"{self.product_type}"
    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        db_table = "insumo"
        ordering = ['id']


class Machine(models.Model):
    supplier_nameM=models.CharField(max_length=50,verbose_name="Nombre proveedor")
    amountM = models.IntegerField(verbose_name="Cantidad")
    machine_type=models.CharField(max_length=20,verbose_name="Tipo maquina")
    description = models.TextField(verbose_name="Descripcion")
    
     #Metodo To String
    def __str__(self) :
        #poner el nombre de campo EJ machine_type
        return f"{self.machine_type}"
    class Meta:
        verbose_name = "Maquina"
        verbose_name_plural = "Maquinas"
        db_table = "maquina"
        ordering = ['id']
#tabla
class Inventory(models.Model):    
    #atributos 
    input = models.ForeignKey(Input,on_delete=models.CASCADE,related_name='Input_product',verbose_name="Insumos")
    machine = models.ForeignKey(Machine,on_delete=models.CASCADE,related_name='Machine_product',verbose_name="Maquinas")


    #Metodo To String
    def __str__(self) :
        return f"Inventario {self.id}"
    #base de datos
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ['id']

