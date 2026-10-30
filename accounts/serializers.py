from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

#phone and pass
class LoginStep1Serializer(serializers.Serializer):
	phone_number = serializers.CharField()
	password 	 = serializers.CharField(write_only=True)

	def  validate(self,data):
		phone 	 = data.get('phone_number')
		password = data.get('password')

		user = authenticate(phone_number=phone,password= password)

		if not user:
			raise serializers.ValidationError("Invalid phone number or password!")

		if not user.is_active:
			raise serializers.ValidationError("This account is disabled. Contact Admin.")

		data['user'] = user
		return data


class LoginStep2Serializer(serializers.Serializer):
	phone_number = serializers.CharField()
	otp = serializers.CharField(max_length=6, min_length=6)

	def validate_otp(self, value):
		if not value.isdigit():
			raise serializers.ValidationError("OTP must contain numbers only.")

		return value