from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginStepOneView, LoginStepTwoVerifyView, RegisterUserView

urlpatterns = [
	
	
	path('register/', RegisterUserView.as_view(), name='register'),
	path('login/', LoginStepOneView.as_view(), name='login_step1'),
	path('login/verify/', LoginStepTwoVerifyView.as_view(), name='login_step2'),

	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]