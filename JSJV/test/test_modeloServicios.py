import pytest
from servicios.models import ProductList

@pytest.mark.django_db
def test_crear_servicio():
    servicio = ProductList.objects.create(
        amount=3,
        description='Jeans',
        status='Ninguno',
        category='Camisa',
    )
    assert servicio.description == 'Jeans'

#pytest --ds=JSJV.settings servicios/tests.py
