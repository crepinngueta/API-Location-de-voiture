from rest_framework import serializers
from account.models import Location, User, Vehicle
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Nous écrivons ceci car nous avons besoin d'un champ de confirmation de mot de passe dans notre requête d'inscription
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc', 'client', 'owner', 'id_card_number', 'driving_license_photo', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validation du mot de passe et du mot de passe de confirmation lors de l'inscription
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Le mot de passe et la confirmation du mot de passe ne correspondent pas")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Le mot de passe et la confirmation du mot de passe ne correspondent pas")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/api/user/reset-password/' + uid + '/' + token + '/'
            body = 'Cliquez sur le lien suivant pour réinitialiser votre mot de passe ' + link
            data = {
                'subject': 'Réinitialiser votre mot de passe',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('Vous n\'êtes pas un utilisateur enregistré')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Le mot de passe et la confirmation du mot de passe ne correspondent pas")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Le jeton n\'est pas valide ou a expiré')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as e:
            raise serializers.ValidationError('Le jeton n\'est pas valide ou a expiré')



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'client', 'owner', 'id_card_number', 'driving_license_photo', 'profile_picture']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.client = validated_data.get('client', instance.client)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.id_card_number = validated_data.get('id_card_number', instance.id_card_number)
        
        # Handling file fields if they are provided in the request
        instance.driving_license_photo = validated_data.get('driving_license_photo', instance.driving_license_photo)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        
        instance.save()
        return instance
    
    
    


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        
        
        
class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address', 'city', 'state', 'zip_code', 'country', 'latitude', 'longitude']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', 'vin', 'kilometers', 'color', 'seats',
                  'location_id', 'available_from', 'available_to', 'price_per_day', 'is_available',
                  'photo_1', 'photo_2', 'photo_3', 'photo_4', 'created_at', 'updated_at']
        


class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin', 'kilometers', 'color', 'seats', 'location_id', 'available_from', 'available_to', 'price_per_day', 'is_available', 'photo_1', 'photo_2', 'photo_3', 'photo_4']
        
        
        
class UserVehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        
        
        
class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__' 
        
        
class AllVehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'  # Inclut tous les champs du modèle Vehicle
        
        



from rest_framework import serializers
from .models import Reservation, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'reservation', 'amount', 'payment_date', 'payment_method']

    def create(self, validated_data):
        # Si la réservation est passée en tant qu'objet, nous utilisons l'ID
        reservation = validated_data.pop('reservation', None)
        if isinstance(reservation, Reservation):
            validated_data['reservation'] = reservation

        payment = Payment.objects.create(**validated_data)
        return payment

class ReservationSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(required=False)

    class Meta:
        model = Reservation
        fields = ['id', 'vehicle', 'start_date', 'end_date', 'reservation_date',
                  'total_cost', 'delivery_location', 'status', 'created_at', 'updated_at', 'payment']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['client'] = request.user  # Associer le client à l'utilisateur actuellement connecté
        payment_data = validated_data.pop('payment', None)
        reservation = Reservation.objects.create(**validated_data)
        if payment_data:
            Payment.objects.create(reservation=reservation, **payment_data)
        return reservation

    def update(self, instance, validated_data):
        payment_data = validated_data.pop('payment', None)
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.reservation_date = validated_data.get('reservation_date', instance.reservation_date)
        instance.total_cost = validated_data.get('total_cost', instance.total_cost)
        instance.delivery_location = validated_data.get('delivery_location', instance.delivery_location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if payment_data:
            payment = instance.payment
            payment.amount = payment_data.get('amount', payment.amount)
            payment.payment_date = payment_data.get('payment_date', payment.payment_date)
            payment.payment_method = payment_data.get('payment_method', payment.payment_method)
            payment.save()

        return instance


from rest_framework import serializers
from .models import Reservation

class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

