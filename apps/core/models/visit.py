from django.db import models


class Visit(models.Model):
    id = models.AutoField(primary_key=True)  # Id
    time_from = models.DateTimeField() # Date and time of beginning of visit
    time_till = models.DateTimeField() # Date and time of end of visit

    #service =  # Provided service
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return (f"{self.id} "
                f"{self.time_from} "
                f"{self.time_till} "
                f"{self.price} "
                )