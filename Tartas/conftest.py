import pytest
from Tartas.models import Tartas, Category


@pytest.fixture
def tartas():
    lst = []
    for i in range(10):
        lst.append(Tartas.objects.create(name=f"Tarta {i}", description="Description", price=i))
    return lst

@pytest.fixture
def categories():
    lst = []
    for i in range(8):
        lst.append(Category.objects.create(name=f"Category {i}"))
    return lst