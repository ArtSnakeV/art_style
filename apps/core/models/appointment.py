from django.db import models

from apps.core.models import Client, Service


class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True)  # BigAutoField for large amount of `id`s
    time_from = models.DateTimeField() # Date and time of beginning of visit
    time_till = models.DateTimeField() # Date and time of end of visit
    appointment_details = models.CharField(max_length=300) # Provided service
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    is_completed = models.BooleanField(False)  # Field to know if appointment passed and service completed

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)



    def __str__(self):
        return (f"{self.id} "
                f"{self.time_from} "
                f"{self.time_till} "
                f"{self.price} "
                f"{self.is_completed}"
                )