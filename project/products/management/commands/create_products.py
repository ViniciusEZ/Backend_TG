from django.core.management.base import BaseCommand
from ... import models
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    def handle(self, *args, **options):
        product = models.Product.objects.get(id=1)
        product_category = models.ProductCategoryDetails.objects.filter(product_id=product.id)
        
        for number in tqdm(range(0, 150000)):
            new_product = models.Product.objects.create(
                name=f'{product.name}_{number}',
                price=product.price,
                quantity=product.quantity,
                image_link=product.image_link,
                category_id=product.category.id,
                supplier_id=product.supplier.id
            )

            for category in product_category:
                new_product_category = models.ProductCategoryDetails.objects.create(
                    product_id=new_product.id,
                    category_details_id=category.category_details.id
                )

