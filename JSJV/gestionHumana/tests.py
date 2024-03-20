#pytest -v --ds=JSJV.settings gestionHumana/tests.py
import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from gestionHumana.models import Schedule, Salary, Activity
from actividades.models import Activity, Novelty, StateAc
from servicios.models import OrderJob,ProductList
from inventario.models import Input,Machine,Inventory
from inventario.models import Inventory
from django.contrib.auth.models import User
from datetime import date, time

#--------------------------------------------- Test destinados a la Creación -----------------------------------------------
@pytest.mark.django_db
def test_creacion_horario_valido():
    # Crear un horario válido con una fecha de ingreso actual
    horario = Schedule.objects.create(
        AdmissionDate=timezone.now().date(),
        startDate=timezone.now().time(),
        finalDate=timezone.now().time()
    )


    assert horario is not None

@pytest.mark.django_db
def test_creacion_salario_valido():
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

    schedule = Schedule.objects.create(
        AdmissionDate=timezone.now().date(),
        startDate=timezone.now().time(),
        finalDate=timezone.now().time()
    )

    # Crear el salario asociado a la actividad y al horario
    salario = Salary.objects.create(
        detailSalary='Detalle del salario',
        descriptionAccount='Descripción de ingresos',
        numberAccount=123456789,  # Ejemplo de número de cuenta
        totalSalary=1000,  # Ejemplo de total de salario
        Activity=actividad,
        schedules=schedule
    )


    assert salario is not None



#--------------------------------------------- Test destinados a la Eliminación -----------------------------------------------
@pytest.mark.django_db
def test_eliminar_horario_valido():
    # Crear un horario válido con una fecha de ingreso actual
    horario = Schedule.objects.create(
        AdmissionDate=timezone.now().date(),
        startDate=timezone.now().time(),
        finalDate=timezone.now().time()
    )

    # Eliminar el horario
    horario.delete()
    
  
    assert not Schedule.objects.filter(pk=horario.pk).exists()

@pytest.mark.django_db
def test_eliminar_salario_valido():
    # Crear instancias necesarias para las relaciones ForeignKey
    novelty = Novelty.objects.create(dateN=date.today(), stateN='Manchado')
    state = StateAc.objects.create(stateAc='Realizada')

    # Crear una instancia de ProductList
    product_list = ProductList.objects.create(amount=3, description='Jeans', status='Ninguno', category='Camisa')

    # Crear una instancia de OrderJob con productList_id proporcionado
    order_job = OrderJob.objects.create(totalPrice=100, dateOT=timezone.now(), productList_id=product_list.id)

    # Crear una instancia de Inventory
    input_obj = Input.objects.create(supplier_nameI='Proveedor1', amountI=10, product_type='Tipo1')
    machine_obj = Machine.objects.create(supplier_nameM='Proveedor2', amountM=5, machine_type='Tipo2', description='Descripción de la máquina')
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

    # Crear un horario asociado al salario
    schedule = Schedule.objects.create(
        AdmissionDate=timezone.now().date(),
        startDate=timezone.now().time(),
        finalDate=timezone.now().time()
    )

    # Crear el salario asociado a la actividad y al horario
    salario = Salary.objects.create(
        detailSalary='Detalle del salario',
        descriptionAccount='Descripción de ingresos',
        numberAccount=123456789,  # Ejemplo de número de cuenta
        totalSalary=1000,  # Ejemplo de total de salario
        Activity=actividad,
        schedules=schedule
    )

    # Eliminar el salario
    salario.delete()


    assert not Salary.objects.filter(pk=salario.pk).exists()

#--------------- Prueva de estres usuarios ----------------------
@pytest.mark.django_db
def test_creacion_100_usuarios():
    # Crear 100 usuarios
    for i in range(100):
        username = f"user{i}"
        password = "password123"
        email = f"user{i}@ejemplo.com"
        User.objects.create_user(username=username, password=password, email=email)

 
    assert User.objects.count() == 100