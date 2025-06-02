from django.db import models


class Account(models.Model):
    id = models.BigAutoField(primary_key=True) # Id
    account_type = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)

    def __str__(self):
        return (f"{self.id} "
                f"{self.account_type} "
                f"{self.account_number} "
                )