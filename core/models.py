from datetime import timezone
from django.db import models
from django.contrib.auth.models import User, Permission  # Import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError  # Import AbstractUser
from .managers import CustomUserManager  # Import CustomUserManager

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    price_range = models.CharField(max_length=5, choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$'), ('$$$$$', '$$$$$')])
    image = models.ImageField(upload_to='hotels/')
    amenities = models.TextField(blank=True, help_text="Comma-separated list of amenities")
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_amenities_list(self):
        return [amenity.strip() for amenity in self.amenities.split(',') if amenity.strip()]

    class Meta:
        permissions = [
            ("change_own_hotel", "Can change own hotel"),
        ]

class Auberge(models.Model):
    TYPE_CHOICES = (
        ('maison', 'Maison'),
        ('camp', 'Camp'),
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    capacite = models.IntegerField()
    nom = models.CharField(max_length=255)
    emplacement = models.CharField(max_length=255, blank=True, null=True)  # Consider using a specialized library for GPS coordinates
    adresse = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # You'll likely want to integrate this with Django's auth system
    telephone = models.CharField(max_length=20)
    nbr_personne_reserve = models.IntegerField(default=0)
    disponibilite = models.BooleanField(default=True)
    image_list = models.JSONField(default=list)  # Store a list of image URLs
    offres = models.JSONField(default=list)  # Store offers as JSON data
    features = models.TextField(blank=True, help_text="Comma-separated list of features")
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auberge', null=True, blank=True)

    def __str__(self):
        return self.nom
    
    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(',') if feature.strip()]

    class Meta:
        permissions = [
            ("change_own_auberge", "Can change own auberge"),
        ]

class Complexe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    price_range = models.CharField(max_length=5, choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$'), ('$$$$$', '$$$$$')])
    image = models.ImageField(upload_to='complexes/')
    area = models.CharField(max_length=50, blank=True)
    facilities = models.TextField(blank=True, help_text="Comma-separated list of facilities")
    accommodation_types = models.CharField(max_length=255, blank=True)
    suitable_for = models.CharField(max_length=255, blank=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complexe', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_facilities_list(self):
        return [facility.strip() for facility in self.facilities.split(',') if facility.strip()]
    
    class Meta:
        permissions = [
            ("change_own_complexe", "Can change own complexe"),
        ]
    
class Transport(models.Model):
    TRANSPORT_TYPES = (
        ('Bus', 'Bus'),
        ('Taxi', 'Taxi'),
        ('Private Transfer', 'Private Transfer'),
    )
    type = models.CharField(max_length=20, choices=TRANSPORT_TYPES)
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    schedule = models.TextField()
    fare = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.type} - {self.name}"

class TouristSpot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tourist_spots/')

    def __str__(self):
        return self.name

class Resident(models.Model):
    SEX_CHOICES = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) # Add this line
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=255)
    sexe = models.CharField(max_length=5, choices=SEX_CHOICES)
    numero_carte_identite = models.CharField(max_length=50, unique=True)
    permission_parentale = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class BlackList(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    numero_carte_identite = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
from django.db.models import Q
from django.utils.timezone import now

class Reservation(models.Model):
    NATURE_CHOICES = (
        ('Gratuit', 'Gratuit'),
        ('Non Gratuit', 'Non Gratuit'),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    auberge = models.ForeignKey(Auberge, on_delete=models.CASCADE, null=True, blank=True)
    complexe = models.ForeignKey(Complexe, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(default=now)  # Correct: Use now without parentheses
    end_date = models.DateField()
    num_rooms = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    nature_reservation = models.CharField(max_length=15, choices=NATURE_CHOICES)
    restauration_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username}"

    def clean(self):
        # Custom validation to ensure only one of hotel, auberge, or complexe is set
        if sum([self.hotel is not None, self.auberge is not None, self.complexe is not None]) != 1:
            raise ValidationError("Exactly one of Hotel, Auberge, or Complexe must be set.")

        # Check for overlapping reservations and room availability
        overlapping_reservations = Reservation.objects.filter(
            Q(hotel=self.hotel) | Q(auberge=self.auberge) | Q(complexe=self.complexe),
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(pk=self.pk)  # Exclude the current reservation if it's being updated

        if overlapping_reservations.exists():
            raise ValidationError("This reservation overlaps with an existing reservation.")

        if self.hotel:
            # Check if enough rooms are available (replace with your logic for Auberge and Complexe)
            if self.hotel.total_rooms - overlapping_reservations.count() < self.num_rooms:
                raise ValidationError("Not enough rooms available for this reservation.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform full model validation before saving
        super().save(*args, **kwargs)
class AubergeResident(models.Model):
    id = models.AutoField(primary_key=True)
    auberge = models.ForeignKey(Auberge, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('auberge', 'resident')  # Ensures a resident can only be associated with an auberge once

    def __str__(self):
        return f"{self.auberge.nom} - {self.resident.nom}"

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auberge = models.ForeignKey(Auberge, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    complexe = models.ForeignKey(Complexe, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars

    class Meta:
        unique_together = ('user', 'auberge', 'hotel', 'complexe')  # User can rate an auberge only once

    def __str__(self):
        if self.auberge:
            target = self.auberge
        elif self.hotel:
            target = self.hotel
        elif self.complexe:
            target = self.complexe
        else:
            target = 'Unknown'
        return f"{self.user.username} rated {target}: {self.rating} stars"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auberge = models.ForeignKey(Auberge, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    complexe = models.ForeignKey(Complexe, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.auberge:
            target = self.auberge
        elif self.hotel:
            target = self.hotel
        elif self.complexe:
            target = self.complexe
        else:
            target = 'Unknown'
        return f"{self.user.username} commented on {target.name}"
    

class Picture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auberge = models.ForeignKey(Auberge, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    complexe = models.ForeignKey(Complexe, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='user_uploads/')

    def __str__(self):
        if self.auberge:
            target = self.auberge
        elif self.hotel:
            target = self.hotel
        elif self.complexe:
            target = self.complexe
        else:
            target = 'Unknown'
        return f"Picture added by {self.user.username} for {target.name}"

# Signal to automatically create or update a Resident when a User is created or updated

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_resident(sender, instance, created, **kwargs):
    if created:
        try:
            # Assuming you have a way to identify blacklisted users (e.g., by national ID)
            blacklisted = BlackList.objects.get(numero_carte_identite=str(instance.pk))
            is_blacklisted = True
        except BlackList.DoesNotExist:
            is_blacklisted = False

        Resident.objects.create(
            user=instance,
            nom="Default Nom",
            prenom="Default Prenom",
            date_naissance="2000-01-01",
            lieu_naissance="Unknown",
            sexe="Homme",
            numero_carte_identite=str(instance.pk),
            is_blacklisted=is_blacklisted  # Set the is_blacklisted field
        )
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_resident(sender, instance, **kwargs):
    try:
        instance.resident.save()
    except Resident.DoesNotExist:
        pass

@receiver(post_save, sender=Hotel)
def assign_hotel_permissions(sender, instance, created, **kwargs):
    if instance.owner and created:
        content_type = ContentType.objects.get_for_model(Hotel)
        permission = Permission.objects.get(
            codename='manage_hotel',  # Use manage_hotel
            content_type=content_type,
        )
        instance.owner.user_permissions.add(permission)

@receiver(post_save, sender=Auberge)
def assign_auberge_permissions(sender, instance, created, **kwargs):
    if instance.owner and created:
        content_type = ContentType.objects.get_for_model(Auberge)
        permission = Permission.objects.get(
            codename='manage_auberge',  # Use manage_auberge
            content_type=content_type,
        )
        instance.owner.user_permissions.add(permission)

@receiver(post_save, sender=Complexe)
def assign_complexe_permissions(sender, instance, created, **kwargs):
    if instance.owner and created:
        content_type = ContentType.objects.get_for_model(Complexe)
        permission = Permission.objects.get(
            codename='manage_complexe',  # Use manage_complexe
            content_type=content_type,
        )
        instance.owner.user_permissions.add(permission)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('auberge_admin', 'Auberge Admin'),
        ('hotel_admin', 'Hotel Admin'),
        ('complexe_admin', 'Complexe Admin'),
        ('transport_admin', 'Transport Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='auberge_admin')
    email = models.EmailField(unique=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # Username is still required for AbstractUser
    
    class Meta:
        permissions = [
            ("manage_auberge", "Can manage assigned auberge"),
            ("manage_hotel", "Can manage assigned hotel"),
            ("manage_complexe", "Can manage assigned complexe"),
            ("manage_transport", "Can manage assigned transport"),
        ]