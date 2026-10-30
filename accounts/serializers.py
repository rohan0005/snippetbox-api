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


class RegisterUserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=6)

	class Meta:
		model=User
		fields = ['id', 'phone_number', 'full_name', 'password']

	def validate_phone_number(self, value):
		if not value.isdigit() or len(value) < 10:
			raise serializers.ValidationError("Enter a valid phone number (at least 10 digits).")
		return value

	def create(self, validated_data):
		user= User.objects.create_user(
			phone_number= validated_data['phone_number'],
			full_name= validated_data.get('full_name', ''),
			password = validated_data['password']
			)
		return user