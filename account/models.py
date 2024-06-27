from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, client, owner, id_card_number,  password=None, password2=None):
        """
        Crée et sauvegarde un utilisateur avec l'email, le nom, tc et mot de passe donnés.
        """
        if not email:
            raise ValueError('L\'utilisateur doit avoir une adresse email')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
            client=client,
            owner=owner,
            id_card_number=id_card_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
        """
        Crée et sauvegarde un superutilisateur avec l'email, le nom, tc et mot de passe donnés.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model
# account/models.py
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)
    id_card_number = models.CharField(max_length=50, unique=True, default='default_value')
    driving_license_photo = models.ImageField(upload_to='licenses/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Location(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}"


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vin = models.CharField(max_length=50, unique=True)
    kilometers = models.IntegerField()
    color = models.CharField(max_length=20)
    seats = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    photo_1 = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"



class Reservation(models.Model):
    STATUS_CHOICES = [
    ('en_attente', 'En attente'),
    ('confirmé', 'Confirmé'),
    ('annulé', 'Annulé'),
    ('terminé', 'Terminé'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reservations')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_reservations')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reservation_date = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation {self.id} for {self.vehicle}"


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=[('stripe', 'Stripe'), ('paypal', 'PayPal')])

    def __str__(self):
        return f"Payment for reservation {self.reservation}"