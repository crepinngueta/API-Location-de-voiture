from django.urls import path,include
from account.views import AddLocationView, UpdateLocationView, UserProfileUpdateView, UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('add-location/', AddLocationView.as_view(), name='add-location'),
    path('update-location/<int:pk>/', UpdateLocationView.as_view(), name='update-location'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]
