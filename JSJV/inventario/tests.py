#pytest -v --ds=JSJV.settings inventario/tests.py

import pytest
from inventario.models import Input,Machine,Inventory
from django.test import TestCase

#------------------------------------- Test destinados a la Creación ------------------------------------------------------
@pytest.mark.django_db
def test_crear_isumo():
    # Crear un nuevo input
    nuevo_input = Input.objects.create(
        supplier_nameI='Proveedor1',
        amountI=10,
        product_type='Tipo1'
    )

    # Verificar si el input se creó correctamente
    assert nuevo_input.supplier_nameI == 'Proveedor1'
    assert nuevo_input.amountI == 10
    assert nuevo_input.product_type == 'Tipo1'

@pytest.mark.django_db
def test_crear_machine():
    # Crear una nueva máquina
    nueva_maquina = Machine.objects.create(
        supplier_nameM='Proveedor1',
        amountM=5,
        machine_type='Tipo1',
        description='Descripción de la máquina'
    )

    # Verificar si la máquina se creó correctamente
    assert nueva_maquina.supplier_nameM == 'Proveedor1'
    assert nueva_maquina.amountM == 5
    assert nueva_maquina.machine_type == 'Tipo1'
    assert nueva_maquina.description == 'Descripción de la máquina'

@pytest.mark.django_db
def test_crear_inventario():
    # Crear instancias de Input y Machine para asociarlas al inventario
    input_obj = Input.objects.create(
        supplier_nameI='Proveedor1',
        amountI=10,
        product_type='Tipo1'
    )

    machine_obj = Machine.objects.create(
        supplier_nameM='Proveedor2',
        amountM=5,
        machine_type='Tipo2',
        description='Descripción de la máquina'
    )

    # Crear una nueva entrada en el inventario
    inventario = Inventory.objects.create(
        input=input_obj,
        machine=machine_obj
    )

    # Verificar si la entrada en el inventario se creó correctamente
    assert inventario.input == input_obj
    assert inventario.machine == machine_obj


#------------------------------------- Test destinados a la Eliminación ------------------------------------------------------

@pytest.mark.django_db
def test_eliminar_insumo():
    # Crear un nuevo insumo
    insumo = Input.objects.create(
        supplier_nameI='Proveedor1',
        amountI=10,
        product_type='Tipo1'
    )

    # Eliminar el insumo
    insumo.delete()

    # Verificar si el insumo se eliminó correctamente
    assert not Input.objects.filter(supplier_nameI='Proveedor1').exists()

@pytest.mark.django_db
def test_eliminar_maquina():
    # Crear una nueva máquina
    maquina = Machine.objects.create(
        supplier_nameM='Proveedor1',
        amountM=5,
        machine_type='Tipo1',
        description='Descripción de la máquina'
    )

    # Eliminar la máquina
    maquina.delete()

    # Verificar si la máquina se eliminó correctamente
    assert not Machine.objects.filter(supplier_nameM='Proveedor1').exists()


@pytest.mark.django_db
def test_eliminar_inventario():
    # Crear instancias de Input y Machine para asociarlas al inventario
    input_obj = Input.objects.create(
        supplier_nameI='Proveedor1',
        amountI=10,
        product_type='Tipo1'
    )

    machine_obj = Machine.objects.create(
        supplier_nameM='Proveedor2',
        amountM=5,
        machine_type='Tipo2',
        description='Descripción de la máquina'
    )

    # Crear una nueva entrada en el inventario
    inventario = Inventory.objects.create(
        input=input_obj,
        machine=machine_obj
    )
    # Eliminar el inventario
    inventario.delete()

    # Verificar si el inventario se eliminó correctamente
    assert not Inventory.objects.filter(id=inventario.id).exists()
