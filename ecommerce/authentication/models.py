from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)


    def generate_otp(self):
        import random
        otp_number = str(random.randint(1000, 9999)) + str(self.id)
        self.otp = otp_number
        self.save()
