from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    price_per_tube = models.IntegerField()
    delivery_days = models.IntegerField()

    def __str__(self):
        return self.name
