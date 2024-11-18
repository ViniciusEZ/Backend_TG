from django.db import models
from django.db.models.functions import Upper
from django.contrib.postgres.indexes import GinIndex, OpClass
from ..acl.models import User
from ..payment.models import Payment_Method

class Supplier(models.Model):
    fantasy_name = models.CharField(db_index=True, max_length=64, unique=True)
    corporate_name = models.CharField(max_length=64)
    cnpj = models.CharField(max_length=14, unique=True)
    contact_phone = models.TextField(unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'products"."supplier'

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'products"."category'


class CategoryDetails(models.Model):
    name = models.CharField(max_length=32)
    about = models.CharField(max_length=64, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'products"."category_details'

class Product(models.Model):
    name = models.CharField(unique=True, max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    quantity = models.PositiveIntegerField(db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    image_link = models.URLField(db_index=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'product'
        indexes = [
            GinIndex(
                OpClass(Upper('name'), name='gin_trgm_ops'),
                name='gin_name_idx'
            )
        ]

        db_table = 'products"."product'

class ProductCategoryDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    category_details = models.ForeignKey(CategoryDetails, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'products"."product_category_details'


class Description(models.Model):
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = 'products"."description'

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    purchase_value = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey(Payment_Method, on_delete=models.PROTECT)

    class Meta:
        db_table='products"."purchase'
