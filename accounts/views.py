import random
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LoginStep1Serializer, LoginStep2Serializer, RegisterUserSerializer
from .models import PhoneOTP
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

User = get_user_model()


class LoginStepOneView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = LoginStep1Serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = serializer.validated_data['user']
		phone_number = user.phone_number

		#generating otp
		generated_otp = str(random.randint(100000, 999999))


		PhoneOTP.objects.update_or_create(phone_number=phone_number,defaults={
			'otp': generated_otp,
			'is_used': False,
			'created_at': timezone.now(),
			} )

		#SMS CODE HERE
		print(f"SMS SENT TO: {phone_number}")

		return Response({
			"details": "Credentials verified. An OTP has been saved and sent to your phone.",
			"otp": generated_otp,
			"phone_number": phone_number
		}, status = status.HTTP_200_OK)


class LoginStepTwoVerifyView(APIView):
	permission_classes = [AllowAny]

	def post(self,request):
		serializer = LoginStep2Serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		phone_number = serializer.validated_data['phone_number']
		user_otp   		 = serializer.validated_data['otp']

		otp_record = PhoneOTP.objects.filter(phone_number=phone_number).first()

		if not otp_record:
			return Response({
				'details': 'No OTP was requested for this phone number.'},
				status=status.HTTP_400_BAD_REQUEST
			)

		if otp_record.is_used:
			return Response({
			"detail": "This OTP has already been used. Please request a new one."},
			status=status.HTTP_400_BAD_REQUEST)

		if otp_record.is_expired():
			return Response(
			{"detail": "OTP has expired. Please log in again to receive a fresh code."},
			status=status.HTTP_400_BAD_REQUEST)

		if otp_record.otp != user_otp:
			return Response (
				{"detail": "Incorrect OTP. Please try again."},
				status=status.HTTP_400_BAD_REQUEST)

		otp_record.is_used = True
		otp_record.save()

		user = User.objects.get(phone_number=phone_number)
		refresh = RefreshToken.for_user(user)


		return Response(
			{
				"detail": "OTP verified successfully. Login complete!",
				"tokens": 
					{
					"refresh": str(refresh),
					"access" : str(refresh.access_token),
					}, 
				"user": {
				'id': user.id,
				"phone_number": user.phone_number,
				}
			},status=status.HTTP_200_OK)


class RegisterUserView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class= RegisterUserSerializer
	permission_classes = [AllowAny]