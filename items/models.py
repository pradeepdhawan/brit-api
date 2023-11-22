from django.db import models

class Item(models.Model):
    name = models.TextField(null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return self.name