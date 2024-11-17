from django.db import models

class Payment_Method(models.Model):
    method = models.CharField(max_length=16)

    class Meta:
        db_table = 'payment"."payment_method'
