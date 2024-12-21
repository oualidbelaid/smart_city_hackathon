from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import (
    Auberge, Resident, BlackList, Reservation,
    AubergeResident, Rating, Comment, Picture,
    Hotel, Complexe, Transport, TouristSpot,
    CustomUser
)
from .forms import CustomUserCreationForm

# Unregister the Group model
admin.site.unregister(Group)

# Define inline admin for related models
class AubergeResidentInline(admin.TabularInline):
    model = AubergeResident
    extra = 1

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'user_type'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'user_type'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'user_type')
    list_filter = ('is_staff', 'is_superuser', 'user_type')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and not obj.is_superuser:  # If editing a user who is not a superuser
            form.base_fields['is_superuser'].disabled = True
        return form

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

@admin.register(Auberge)
class AubergeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'capacite', 'adresse', 'email', 'telephone', 'disponibilite')
    search_fields = ('nom', 'adresse', 'email')
    list_filter = ('type', 'disponibilite')
    inlines = [AubergeResidentInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'sexe', 'numero_carte_identite')
    search_fields = ('nom', 'prenom', 'numero_carte_identite')
    list_filter = ('sexe',)

@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'numero_carte_identite')
    search_fields = ('nom', 'prenom', 'numero_carte_identite')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_reservation_type', 'get_related_name', 'user', 'start_date', 'end_date', 'nature_reservation')
    search_fields = ('user__username', 'hotel__name', 'auberge__nom', 'complexe__name')
    list_filter = ('nature_reservation', 'start_date', 'end_date')

    def get_reservation_type(self, obj):
        if obj.hotel:
            return 'Hotel'
        elif obj.auberge:
            return 'Auberge'
        elif obj.complexe:
            return 'Complexe'
        return 'Unknown'
    get_reservation_type.short_description = 'Type'

    def get_related_name(self, obj):
        if obj.hotel:
            return obj.hotel.name
        elif obj.auberge:
            return obj.auberge.nom
        elif obj.complexe:
            return obj.complexe.name
        return 'Unknown'
    get_related_name.short_description = 'Related Name'

@admin.register(AubergeResident)
class AubergeResidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'auberge', 'resident')
    search_fields = ('auberge__nom', 'resident__nom', 'resident__prenom')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_target_name', 'rating')
    list_filter = ('rating',)

    def get_target_name(self, obj):
        if obj.auberge:
            return f"{obj.auberge.nom} (Auberge)"
        elif obj.hotel:
            return f"{obj.hotel.name} (Hotel)"
        elif obj.complexe:
            return f"{obj.complexe.name} (Complexe)"
        return "Unknown"
    get_target_name.short_description = 'Target'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_target_name', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment',)

    def get_target_name(self, obj):
        if obj.auberge:
            return f"{obj.auberge.nom} (Auberge)"
        elif obj.hotel:
            return f"{obj.hotel.name} (Hotel)"
        elif obj.complexe:
            return f"{obj.complexe.name} (Complexe)"
        return "Unknown"
    get_target_name.short_description = 'Target'

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_target_name', 'image')

    def get_target_name(self, obj):
        if obj.auberge:
            return f"{obj.auberge.nom} (Auberge)"
        elif obj.hotel:
            return f"{obj.hotel.name} (Hotel)"
        elif obj.complexe:
            return f"{obj.complexe.name} (Complexe)"
        return "Unknown"
    get_target_name.short_description = 'Target'

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', 'price_range')
    search_fields = ('name', 'description')
    list_filter = ('stars', 'price_range')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Complexe)
class ComplexeAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', 'price_range')
    search_fields = ('name', 'description')
    list_filter = ('stars', 'price_range')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'route', 'fare')
    search_fields = ('name', 'route')
    list_filter = ('type',)

@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

# Register the CustomUser
admin.site.register(CustomUser, CustomUserAdmin)