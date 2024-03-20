#pytest -v --ds=JSJV.settings test/gestionHumana.py
import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from gestionHumana.models import Schedule, Salary, Activity
from actividades.models import Activity, Novelty, StateAc
from servicios.models import OrderJob,ProductList
from inventario.models import Input,Machine,Inventory
from inventario.models import Inventory
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

    # Verificar que se creó el horario correctamente
    assert horario is not None

@pytest.mark.django_db
def test_creacion_salario_valido():
    # Crear instancias necesarias para las relaciones ForeignKey
    novelty = Novelty.objects.create(dateN=date.today(), stateN='Manchado')
    state = StateAc.objects.create(stateAc='Realizada')
    product_list = ProductList.objects.create(amount=3, description='Jeans',status='Ninguno', category='Camisa')
    order_job = OrderJob.objects.create(totalPrice=100, dateOT=date.today(), productList_id=product_list.id)
    input_instance = Input.objects.create(supplier_nameI='Proveedor1',amountI=10, product_type='Tipo1')
    machine_instance = Machine.objects.create(supplier_nameM='Proveedor2',amountM=5,machine_type='Tipo2',description='Descripción de la máquina')
    inventory = Inventory.objects.create(input=input_instance, machine=machine_instance)
    
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
    
    # Asegurarse de que la actividad se creó correctamente
    assert actividad is not None