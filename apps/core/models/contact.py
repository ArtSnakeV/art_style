from django.db import models


class Contact(models.Model):

    id = models.AutoField(primary_key=True) # Id

    contact_type = models.CharField(max_length=21) # phone, telegram, etc

    contact_value = models.CharField(max_length=21) # value

    def __str__(self):
        return (f"{self.id} "
                f"{self.contact_type} "
                f"{self.contact_value} "
                )

