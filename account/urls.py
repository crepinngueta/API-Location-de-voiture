from django.urls import path,include
from account.views import VehicleListByTypeView, AddLocationView, AddVehicleView, AllVehiclesListView, DeleteVehicleView, PaymentCreateView, ReservationView, UpdateLocationView, UpdateVehicleView, UserProfileUpdateView, UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView, UserReservationsView, UserVehiclesListAPIView, VehicleDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('add-location/', AddLocationView.as_view(), name='add-location'),
    path('add-vehicle/', AddVehicleView.as_view(), name='add-vehicle'),
    path('delete-vehicle/<int:pk>/', DeleteVehicleView.as_view(), name='delete_vehicle'),
    path('update-vehicle/<int:pk>/', UpdateVehicleView.as_view(), name='update-vehicle'),
    path('update-location/<int:pk>/', UpdateLocationView.as_view(), name='update-location'),
    path('vehicles/', UserVehiclesListAPIView.as_view(), name='user-vehicles-list'),
    path('vehicle-details/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('all-vehicles/', AllVehiclesListView.as_view(), name='all-vehicles'),
    path('reserve-vehicle/', ReservationView.as_view(), name='reserve-vehicle'),
    path('payment/', PaymentCreateView.as_view(), name='payment-create'),
    path('my-reservations/', UserReservationsView.as_view(), name='user-reservations'),
    path('vehicles/type/<str:vehicle_type>/', VehicleListByTypeView.as_view(), name='vehicles-by-type'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)