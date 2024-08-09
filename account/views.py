from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.models import Location, Payment, Reservation, Vehicle
from account.serializers import AllVehiclesSerializer, ContactSerializer, LocationSerializer, LocationUpdateSerializer, OwnerReservationSerializer, PaymentSerializer, ReservationSerializer, ReservationSerializers, ReservationStatusUpdateSerializer, UserProfileUpdateSerializer, UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer, UserVehiclesSerializer, VehicleDetailSerializer, VehicleSerializer, VehicleUpdateSerializer, VehicleTypeSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Contact, User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

  
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  

class UserProfileUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
      
class UpdateLocationView(APIView):
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationUpdateSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Location updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
class AddVehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.owner:
            return Response({'error': 'Vous devez être propriétaire pour ajouter un véhicule.'}, status=status.HTTP_403_FORBIDDEN)

        # Utilisation du serializer pour valider et sauvegarder les données
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            # Sauvegarde de l'objet véhicule avec l'ID du propriétaire
            vehicle = serializer.save(owner_id=request.user.id)

            # Récupération des URLs absolues des images si elles existent
            image_urls = {
                'photo_1': request.build_absolute_uri(vehicle.photo_1.url) if vehicle.photo_1 else '',
                'photo_2': request.build_absolute_uri(vehicle.photo_2.url) if vehicle.photo_2 else '',
                'photo_3': request.build_absolute_uri(vehicle.photo_3.url) if vehicle.photo_3 else '',
                'photo_4': request.build_absolute_uri(vehicle.photo_4.url) if vehicle.photo_4 else '',
            }

            return Response({'msg': 'Véhicule ajouté avec succès', 'image_urls': image_urls}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
      
      
class UpdateVehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        vehicle = self.get_object(pk)
        # Check if the current user is the owner of the vehicle
        if not request.user.owner:
            return Response({'error': 'You are not authorized to update this vehicle'}, status=status.HTTP_403_FORBIDDEN)

        serializer = VehicleUpdateSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Vehicle updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteVehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404

        # Vérifier si l'utilisateur actuel est le propriétaire du véhicule
        if vehicle.owner_id != request.user.id:
            return Response({'error': 'Vous n\'êtes pas autorisé à supprimer ce véhicule.'}, status=status.HTTP_403_FORBIDDEN)

        vehicle.delete()
        return Response({'msg': 'Véhicule supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)
      
      
      
      
      
      
class UserVehiclesListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Récupère l'utilisateur actuel authentifié
        vehicles = Vehicle.objects.filter(owner=user)
        serializer = UserVehiclesSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
      

class VehicleDetailView(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailSerializer
    permission_classes = [IsAuthenticated] 
    
    
    
class AllVehiclesListView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = AllVehiclesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    
class ReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ReservationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Réservation créée avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Récupérer l'utilisateur actuellement connecté
        user = request.user

        # Récupérer les données de la requête
        data = request.data

        # Imprimer les données reçues pour le débogage
        print("Données de la requête:", data)

        # Vérifier que la clé 'reservation' est présente dans les données de la requête
        if 'reservation' not in data:
            return Response({"error": "La clé 'reservation' est manquante."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que la réservation existe et que l'utilisateur est le client de la réservation
        try:
            reservation = Reservation.objects.get(id=data['reservation'], client=user)
        except Reservation.DoesNotExist:
            return Response({"error": "Réservation non trouvée ou vous n'êtes pas le client de cette réservation."}, status=status.HTTP_404_NOT_FOUND)

        # Utiliser le montant total de la réservation pour le paiement
        payment_data = {
            'reservation': reservation.id,
            'amount': reservation.total_cost,
            'payment_method': data.get('payment_method')
        }

        # Créer le paiement
        serializer = self.get_serializer(data=payment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reservation=reservation)  # Lier la réservation au paiement

        return Response({"msg": "Paiement réussi"}, status=status.HTTP_201_CREATED)
      


class UserReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reservations = Reservation.objects.filter(client=user)
        serializer = ReservationSerializers(reservations, many=True)
        return Response(serializer.data)
      
      
      
class VehicleListByTypeView(generics.ListAPIView):
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        vehicle_type = self.kwargs['vehicle_type']
        return Vehicle.objects.filter(vehicle_type=vehicle_type)
    
    
import googlemaps
from django.conf import settings
    
def get_geocode(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        return geocode_result[0]['geometry']['location']
    return None    

from .utils import get_geocode

class CreateLocationFromAddress(APIView):
    def post(self, request):
        address = request.data.get('address')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        location = Location.create_from_address(user, address, latitude, longitude)

        if location:
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid address'}, status=status.HTTP_400_BAD_REQUEST) 
    
import stripe    
 
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = int(request.data.get('amount'))  # Montant en centimes
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({'client_secret': intent.client_secret})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client_contact=self.request.user)
    
             
             

class OwnerReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            owner = request.user
            vehicles = Vehicle.objects.filter(owner=owner)
            reservations = Reservation.objects.filter(vehicle__in=vehicles)
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateReservationStatusView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        reservation = self.get_object()
        # Vous pouvez ajouter des vérifications supplémentaires ici si nécessaire
        if reservation.client != request.user and reservation.vehicle.owner != request.user:
            return Response({'detail': 'You do not have permission to update this reservation.'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().patch(request, *args, **kwargs)                

from django.db.models import Count
from django.shortcuts import render

def statistics_view(request):
    # Exemple de données statistiques : Nombre de réservations par statut
    reservation_stats = Reservation.objects.values('status').annotate(count=Count('status'))

    # Préparez les données pour Chart.js
    labels = [stat['status'] for stat in reservation_stats]
    data = [stat['count'] for stat in reservation_stats]

    context = {
        'labels': labels,
        'data': data
    }
    return render(request, 'admin/statistics.html', context)