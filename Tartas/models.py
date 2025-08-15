from django.db import models

# Create your models here.

CATEGORIES = (
    (1, 'A base de bizcocho tradicional'),
    (2, 'A base de bizcocho con pistacho'),
    (3, 'A base de bizcocho de almendra'),
    (4, 'A base de bizcocho con cafe'),
    (5, 'Tartas Veganas tipo Loaf'),
    (6, 'Gluten-free'),
    (7, 'Brownie'),
    (8, 'Otros'),
)

class Category(models.Model):
    name = models.IntegerField(choices=CATEGORIES, blank=True, null=True)

    def __str__(self):
        return str(self.get_name_display())

class Tartas(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ManyToManyField(Category, blank=True)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)

    @staticmethod
    def get_products_by_id(ids):
        return Tartas.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Tartas.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Tartas.objects.filter(category=category_id)
        else:
            return Tartas.get_all_products()

    def __str__(self):
        return self.name
