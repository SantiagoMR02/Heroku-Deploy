#pytest -v --ds=JSJV.settings actividades/tests.py

from django.utils import timezone
from actividades.models import Activity, StateAc, Novelty
from inventario.models import Inventory, Input, Machine
from servicios.models import OrderJob, ProductList
import pytest
from datetime import date, time

#------------------------------------- Test destinados a la Creación ------------------------------------------------------
@pytest.mark.django_db
def test_creacion_estado_actividad():
    # Crear una instancia de StateAc
    estado = StateAc.objects.create(stateAc='Realizada')

    assert estado is not None


@pytest.mark.django_db
def test_creacion_novedad():
    # Crear una instancia de Novelty
    novedad = Novelty.objects.create(dateN=date.today(), stateN='Manchado')


    assert novedad is not None

@pytest.mark.django_db
def test_creacion_actividad():
    # Crear instancias necesarias para las relaciones ForeignKey
    novelty = Novelty.objects.create(dateN=date.today(), stateN='Manchado')
    state = StateAc.objects.create(stateAc='Realizada')

    # Crear una instancia de ProductList
    product_list = ProductList.objects.create(amount=3, description='Jeans', status='Ninguno', category='Camisa')

    # Crear una instancia de OrderJob con productList_id proporcionado
    order_job = OrderJob.objects.create(totalPrice=100, dateOT=timezone.now(), productList_id=product_list.id)

    # Crear una instancia de Inventory
    input_obj = Input.objects.create(supplier_nameI='Proveedor1',amountI=10,product_type='Tipo1')
    machine_obj = Machine.objects.create(supplier_nameM='Proveedor2',amountM=5,machine_type='Tipo2',description='Descripción de la máquina')
    inventory = Inventory.objects.create(input=input_obj, machine=machine_obj)
    
    # Crear la actividad asociada al salario
    actividad = Activity.objects.create(
        dateAc=date.today(),
        timeAc=time(8, 0),  # Hora ficticia
        descriptionAc='Descripción de prueba',
        noveltyAc=novelty,
        stateAc=state,
        orderJob=order_job,
        inventory=inventory,
        ActivityValue=50.0
    )
    
 
    assert actividad is not None

#------------------------------------- Test destinados a la Eliminación ------------------------------------------------------

@pytest.mark.django_db
def test_eliminar_estado_actividad():
    # Crear una instancia de StateAc
    estado = StateAc.objects.create(stateAc='Realizada')

    # Asegurar que la instancia se creó correctamente
    assert estado is not None

    estado.delete()
   
    assert StateAc.objects.filter(pk=estado.pk).exists() is False

@pytest.mark.django_db
def test_eliminar_novedad():
    # Crear una instancia de Novelty
    novedad = Novelty.objects.create(dateN=date.today(), stateN='Manchado')

    # Asegurar que la instancia se creó correctamente
    assert novedad is not None

    # Eliminar la instancia
    novedad.delete()

   
    assert Novelty.objects.filter(pk=novedad.pk).exists() is False

@pytest.mark.django_db
def test_eliminar_actividad():
    # Crear instancias necesarias para las relaciones ForeignKey
    novelty = Novelty.objects.create(dateN=date.today(), stateN='Manchado')
    state = StateAc.objects.create(stateAc='Realizada')

    # Crear una instancia de ProductList
    product_list = ProductList.objects.create(amount=3, description='Jeans', status='Ninguno', category='Camisa')

    # Crear una instancia de OrderJob con productList_id proporcionado
    order_job = OrderJob.objects.create(totalPrice=100, dateOT=timezone.now(), productList_id=product_list.id)

    # Crear una instancia de Inventory
    input_obj = Input.objects.create(supplier_nameI='Proveedor1',amountI=10,product_type='Tipo1')
    machine_obj = Machine.objects.create(supplier_nameM='Proveedor2',amountM=5,machine_type='Tipo2',description='Descripción de la máquina')
    inventory = Inventory.objects.create(input=input_obj, machine=machine_obj)
    
    # Crear la actividad asociada al salario
    actividad = Activity.objects.create(
        dateAc=date.today(),
        timeAc=time(8, 0),  # Hora ficticia
        descriptionAc='Descripción de prueba',
        noveltyAc=novelty,
        stateAc=state,
        orderJob=order_job,
        inventory=inventory,
        ActivityValue=50.0
    )

    # Eliminar la actividad
    actividad.delete()
    
    assert not Activity.objects.filter(pk=actividad.pk).exists()