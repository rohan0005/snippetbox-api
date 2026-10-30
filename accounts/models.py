from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
	def create_user(self, phone_number, password=None, **extra_fields):
		if not phone_number:
			raise ValueError("The Phone Number must be provided")

		user = self.model(phone_number=phone_number,**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
	username = None

	phone_number = models.CharField(max_length=15,unique=True)
	full_name = models.CharField(max_length=100, blank=True)

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELD = []

	objects = CustomUserManager()

	def __str__(self):
		return self.phone_number


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