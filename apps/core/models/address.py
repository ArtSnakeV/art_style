from django.db import models

class Address(models.Model):
    id = models.BigAutoField(primary_key=True)  # Id
    country = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=5)
    flat = models.CharField(max_length=5)

    # Методи
    def __str__(self):
        return (f"{self.id}"
                f"{self.country} "
                f"{self.region} "
                f"{self.district} "
                f"{self.street} "
                f"{self.house} "
                f"{self.flat} "
                )



