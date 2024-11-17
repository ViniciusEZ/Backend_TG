# Generated by Django 5.1.2 on 2024-11-16 20:59

import django.contrib.postgres.indexes
import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'products"."category',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fantasy_name', models.CharField(db_index=True, max_length=64, unique=True)),
                ('corporate_name', models.CharField(max_length=64)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('contact_phone', models.TextField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'db_table': 'products"."supplier',
            },
        ),
        migrations.CreateModel(
            name='CategoryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('about', models.CharField(max_length=64, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='products.category')),
            ],
            options={
                'db_table': 'products"."category_details',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('image_link', models.URLField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='products.category')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.supplier')),
            ],
            options={
                'db_table': 'products"."product',
            },
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
            options={
                'db_table': 'products"."description',
            },
        ),
        migrations.CreateModel(
            name='ProductCategoryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_details', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.categorydetails')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
            options={
                'db_table': 'products"."product_category_details',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('purchase_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment.payment_method')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'products"."purchase',
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.indexes.OpClass(django.db.models.functions.text.Upper('name'), name='gin_trgm_ops'), name='gin_name_idx'),
        ),
    ]
