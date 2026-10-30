from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class PhoneOTP(models.Model):
	phone_number = models.CharField(max_length=15)
	otp = models.CharField(max_length=6)
	created_at = models.DateTimeField(auto_now_add=True)
	is_used = models.BooleanField(default=False)

	def is_expired(self):
		""" returns true if OTP is older than 5 minutes """
		expiration_time = self.created_at + timedelta(minutes=5)
		return timezone.now() > expiration_time

	def __str__(self):
		return f"{self.phone_number} - {self.otp}"