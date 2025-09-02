from django.db import models
from django.utils import timezone
from datetime import timedelta
from utility.utils import get_otp_expirity

class OTP(models.Model):
    """
    Base Class for storing OTP generated as
    a part of validating mobile number
    """
    otp_number = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    expiry_time = models.DateTimeField(default=get_otp_expirity)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'otp'

    def save(self, *args, **kwargs):
        data = OTP.objects.filter(email=self.email)
        data.delete()
        super(OTP, self).save(*args, **kwargs)
