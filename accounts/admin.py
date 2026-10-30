from django.contrib import admin
from .models import User, PhoneOTP
# Register your models here.


admin.site.register(User)

@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'otp', 'created_at', 'is_used')
	search_fields = ('phone_number',)

