from django.db import models

class Speciality(models.Model):
    id = models.AutoField(primary_key=True)
    speciality_name = models.CharField(21)

    def __str__(self):
        return (f"{self.id} "
                f"{self.speciality_name} "
                )