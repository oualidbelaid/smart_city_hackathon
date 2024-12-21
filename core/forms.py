from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resident, Hotel, Transport, Rating, Comment, Picture
from .models import CustomUser, Resident

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only superusers can set user_type
        if not kwargs.get('initial', {}).get('is_superuser'):
            self.fields['user_type'].widget = forms.HiddenInput()

class PropertyAdminAssignmentForm(forms.Form):
    admin_user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_superuser=False),
        required=True,
        label="Select Admin User"
    )
    
    def __init__(self, *args, property_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        if property_type:
            self.fields['admin_user'].queryset = CustomUser.objects.filter(
                user_type=f'{property_type}_admin',
                is_superuser=False
            )
# Other forms
class HotelFilterForm(forms.Form):
    stars = forms.IntegerField(required=False, widget=forms.Select(choices=[(None, 'Any'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]))
    price_range = forms.CharField(required=False, widget=forms.Select(choices=[(None, 'Any'), ('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$'), ('$$$$$', '$$$$$')]))
    amenities = forms.CharField(required=False)

class TransportFilterForm(forms.Form):
    type = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    schedule = forms.CharField(required=False)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image']


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Import your custom user model

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Resident

class UserRegistrationForm(UserCreationForm):
    # Fields for the CustomUser model
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    # Fields for the Resident model
    numero_carte_identite = forms.CharField(label="National ID Number")
    sexe = forms.ChoiceField(label="Sex", choices=Resident.SEX_CHOICES)
    date_naissance = forms.DateField(label="Date of Birth", widget=forms.SelectDateWidget(years=range(1920, 2023))) # Adjust year range as needed
    lieu_naissance = forms.CharField(label="Place of Birth")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'numero_carte_identite', 'sexe', 'date_naissance', 'lieu_naissance']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        # Create or update Resident
        resident, created = Resident.objects.get_or_create(user=user)
        resident.numero_carte_identite = self.cleaned_data['numero_carte_identite']
        resident.sexe = self.cleaned_data['sexe']
        resident.date_naissance = self.cleaned_data['date_naissance']
        resident.lieu_naissance = self.cleaned_data['lieu_naissance']
        resident.nom = self.cleaned_data['last_name']
        resident.prenom = self.cleaned_data['first_name']
        # Set other fields for Resident
        if commit:
            resident.save()

        return user


# forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'password')  # Customize if needed
from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'num_rooms', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }