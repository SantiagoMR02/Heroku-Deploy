
#pytest -v --ds=JSJV.settings servicios/tests.py
#pip install pytest-django

import pytest
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # Aquí importas timezone desde django.utils

from datetime import date 

from servicios.models import ProductList, TypeService, OrderJob, OutputOJ, Income


@pytest.mark.django_db
def test_crear_producto():
    servicio = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )
    assert servicio.description == 'Jeans'

@pytest.mark.django_db
def test_crear_tipo_servicio():
    # Crear un nuevo tipo de servicio
    nuevo_tipo_servicio = TypeService.objects.create(
        descriptionTS='Lavanteria'
    )

    # Verificar si el tipo de servicio se creó correctamente
    assert nuevo_tipo_servicio.descriptionTS == 'Lavanteria'
    
@pytest.mark.django_db
def test_crear_order_job():
    # Crear un nuevo producto para asociarlo a la orden de trabajo
    producto = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )
    
    # Obtener la fecha actual
    fecha_actual = date.today()

    # Crear una nueva orden de trabajo con la fecha actual
    order_job = OrderJob.objects.create(
        totalPrice=100,
        dateOT=fecha_actual,
        productList=producto
    )

    # Verificar si la orden de trabajo se creó correctamente
    assert order_job.totalPrice == 100
    assert order_job.dateOT == fecha_actual
    assert order_job.productList == producto

@pytest.mark.django_db
def test_crear_output_oj():
    # Crear un nuevo producto para asociarlo a la salida OT
    producto = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )

    # Crear una nueva salida OT
    output_oj = OutputOJ.objects.create(
        productList=producto,
        amountOutputs=2,
        dateOutput=None  
    )

    # Verificar si la salida OT se creó correctamente
    assert output_oj.productList == producto
    assert output_oj.amountOutputs == 2
    assert output_oj.dateOutput is None  # La fecha debe ser None

@pytest.mark.django_db
def test_crear_ingreso():
    # Crear un nuevo producto para asociarlo a la orden de trabajo
    producto = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )

    # Crear una nueva orden de trabajo con la fecha y hora actual
    orden_trabajo = OrderJob.objects.create(
        totalPrice=100,
        dateOT=timezone.now(),  # Utiliza timezone.now() para obtener la fecha y hora actuales
        productList=producto  # Asocia la orden de trabajo con el producto creado
    )

    # Crear un nuevo ingreso asociado a la orden de trabajo
    ingreso = Income.objects.create(
        paymentMethod='Efectivo',  # Método de pago válido
        descriptionIncome='Venta de productos',
        totalincome=200.0,
        orderJob=orden_trabajo  # Asocia el ingreso con la orden de trabajo creada
    )

    # Verificar si el ingreso se creó correctamente
    assert ingreso.paymentMethod == 'Efectivo'
    assert ingreso.descriptionIncome == 'Venta de productos'
    assert ingreso.totalincome == 200.0
    assert ingreso.orderJob == orden_trabajo

@pytest.mark.django_db
def test_eliminar_producto():
    # Crear un producto para eliminar
    producto = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )

    # Eliminar el producto
    producto.delete()

    # Verificar si el producto se eliminó correctamente
    assert not ProductList.objects.filter(description='Jeans').exists()

@pytest.mark.django_db
def test_eliminar_tipo_servicio():
    # Crear un tipo de servicio para eliminar
    tipo_servicio = TypeService.objects.create(
        descriptionTS='Lavanteria'
    )

    # Eliminar el tipo de servicio
    tipo_servicio.delete()

    # Verificar si el tipo de servicio se eliminó correctamente
    assert not TypeService.objects.filter(descriptionTS='Lavanteria').exists()


@pytest.mark.django_db
def test_eliminar_output_oj():
    # Crear un objeto ProductList
    producto = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )

    # Crear un objeto OutputOJ asociado al objeto ProductList creado
    output_oj = OutputOJ.objects.create(
        productList=producto,  # Asociar el producto creado anteriormente
        amountOutputs=2,
        dateOutput=None
    )

    # Verificar si el objeto OutputOJ se creó correctamente
    assert output_oj.productList == producto
    assert output_oj.amountOutputs == 2
    assert output_oj.dateOutput is None

@pytest.mark.django_db
def test_eliminar_ingreso():
    # Crear un objeto ProductList válido
    producto = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )

    # Crear una orden de trabajo con el producto creado
    orden_trabajo = OrderJob.objects.create(
        totalPrice=100,
        dateOT="2024-03-07",  # Fecha ficticia
        productList=producto  # Asignar el producto creado
    )
    # Crear un ingreso asociado a la orden de trabajo
    ingreso = Income.objects.create(
        paymentMethod='Efectivo',
        descriptionIncome='Venta de productos',
        totalincome=200.0,
        orderJob=orden_trabajo
    )

    # Verificar que el ingreso se haya creado correctamente
    assert Income.objects.filter(paymentMethod='Efectivo').exists()

    # Eliminar el ingreso
    ingreso.delete()

    # Verificar que el ingreso se haya eliminado correctamente
    with pytest.raises(ObjectDoesNotExist):
        Income.objects.get(paymentMethod='Efectivo')