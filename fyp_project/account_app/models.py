from django.db import models


class RegisterUser(models.Model):
    email = models.CharField(max_length=250, primary_key=True)
    password = models.CharField(max_length=250)
    def __str__(self):
        return self.email
