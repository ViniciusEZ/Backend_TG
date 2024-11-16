from django.db import models

class Supplier(models.Model):
    fantasy_name = models.CharField(max_length=64, unique=True)
    corporate_name = models.CharField(max_length=64)
    cnpj = models.CharField(max_length=14, unique=True)
    contact_phone = models.TextField(unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'supplier'

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'category'


class CategoryDetails(models.Model):
    name = models.CharField(max_length=32)
    about = models.CharField(max_length=64, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'category_details'

class Product(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    image_link = models.URLField()
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'product'

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    category_details = models.ForeignKey(CategoryDetails, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'product_category'


class Description(models.Model):
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = 'description'





# class Purchase(models.Model):
#     ...