from django.db import models


class Service(models.Model):
    id = models.AutoField(primary_key=True)  # Id
    service_title = models.CharField(50)
    service_description = models.CharField(50)
    service_price= models.DecimalField(max_digits=8, decimal_places=2, default=0)


# Методи
    def __str__(self):
        return (f"{self.id} "
                f"{self.service_title} "
                f"{self.service_description} "
                f"{self.service_price} "
                )