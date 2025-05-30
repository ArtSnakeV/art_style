from django.db import models

# from apps.core.models import Client, Specialist


class Contact(models.Model):

    id = models.AutoField(primary_key=True) # Id

    contact_type = models.CharField(max_length=21) # phone, telegram, etc

    contact_value = models.CharField(max_length=21) # value

    # client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts', null=True)  # Add this line
    #
    # specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='contacts', null=True)  # Add this line

    def __str__(self):
        return (f"{self.id} "
                f"{self.contact_type} "
                f"{self.contact_value} "
                )

