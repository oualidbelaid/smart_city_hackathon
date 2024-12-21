from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Transport, Auberge, Complexe, Rating, Comment, Picture
from django.db.models import Q
from .forms import HotelFilterForm, TransportFilterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Auberge, Hotel, Complexe, Rating, Comment, Picture
from .forms import RatingForm, CommentForm, PictureForm


from django.shortcuts import render, get_object_or_404
from .models import Hotel, Transport, Auberge, Complexe
from django.db.models import Q
from .forms import HotelFilterForm, TransportFilterForm

def hotel_list(request):
    hotels = Hotel.objects.all()
    form = HotelFilterForm(request.GET)

    if form.is_valid():
        stars = form.cleaned_data.get('stars')
        price_range = form.cleaned_data.get('price_range')
        amenities = form.cleaned_data.get('amenities')

        if stars:
            hotels = hotels.filter(stars=stars)
        if price_range:
            hotels = hotels.filter(price_range=price_range)
        if amenities:
            for amenity in amenities:
                hotels = hotels.filter(amenities__icontains=amenity)

    context = {
        'hotels': hotels,
        'form': form,
    }
    return render(request, 'core/hotel_list.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotel, Auberge, Complexe, Reservation
from .forms import ReservationForm

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    form = ReservationForm()  # Initialize the form outside the if block
    context = {
        'hotel': hotel,
        'form': form,
    }
    return render(request, 'core/hotel_detail.html', context)

def transport(request):
    transports = Transport.objects.all()
    form = TransportFilterForm(request.GET)

    if form.is_valid():
        type = form.cleaned_data.get('type')
        destination = form.cleaned_data.get('destination')
        schedule = form.cleaned_data.get('schedule')

        if type:
            transports = transports.filter(type=type)
        if destination:
            transports = transports.filter(Q(route__icontains=destination) | Q(name__icontains=destination))

        if schedule:
            transports = transports.filter(schedule__icontains=schedule)

    context = {'transports': transports, 'form': form}
    return render(request, 'core/transport.html', context)

def auberge_list(request):
    auberges = Auberge.objects.all()
    # You can add filtering logic here, similar to hotel_list

    context = {
        'auberges': auberges,
    }
    return render(request, 'core/auberge_list.html', context)

def complexe_list(request):
    complexes = Complexe.objects.all()
    # You can add filtering logic here, similar to hotel_list

    context = {
        'complexes': complexes,
    }
    return render(request, 'core/complexe_list.html', context)

@login_required  # Ensure the user is logged in
def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'core/profile.html', context)


from django.shortcuts import render

def index(request):
    return render(request, 'core/home.html')

def hotel_list(request):
    hotels = Hotel.objects.all()
    form = HotelFilterForm(request.GET)

    if form.is_valid():
        stars = form.cleaned_data.get('stars')
        price_range = form.cleaned_data.get('price_range')
        amenities = form.cleaned_data.get('amenities')

        if stars:
            hotels = hotels.filter(stars=stars)
        if price_range:
            hotels = hotels.filter(price_range=price_range)
        if amenities:
            for amenity in amenities:
                hotels = hotels.filter(amenities__icontains=amenity)

    context = {
        'hotels': hotels,
        'form': form,
    }
    return render(request, 'core/hotel_list.html', context)

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'core/hotel_detail.html', {'hotel': hotel})

def transport(request):
    transports = Transport.objects.all()
    form = TransportFilterForm(request.GET)

    if form.is_valid():
        type = form.cleaned_data.get('type')
        destination = form.cleaned_data.get('destination')
        schedule = form.cleaned_data.get('schedule')

        if type:
            transports = transports.filter(type=type)
        if destination:
            transports = transports.filter(Q(route__icontains=destination) | Q(name__icontains=destination))

        if schedule:
            transports = transports.filter(schedule__icontains=schedule)

    context = {'transports': transports, 'form': form}
    return render(request, 'core/transport.html', context)

def auberge_list(request):
    auberges = Auberge.objects.all()
    # You can add filtering logic here, similar to hotel_list

    context = {
        'auberges': auberges,
    }
    return render(request, 'core/auberge_list.html', context)

def complexe_list(request):
    complexes = Complexe.objects.all()
    # You can add filtering logic here, similar to hotel_list

    context = {
        'complexes': complexes,
    }
    return render(request, 'core/complexe_list.html', context)

def profile(request):
    # Placeholder for user profile view.
    # You'll need to implement authentication and user-specific data retrieval.
    context = {
        'user': request.user,  # Assuming you have user authentication set up
    }
    return render(request, 'core/profile.html', context)

@login_required
def rate_object(request, object_type, object_id):
    user = request.user
    rating_value = request.POST.get('rating')

    model = {
        'auberge': Auberge,
        'hotel': Hotel,
        'complexe': Complexe
    }.get(object_type)

    if not model:
        # Handle invalid object type
        return redirect('/') # Or to an error page

    obj = get_object_or_404(model, pk=object_id)

    rating, created = Rating.objects.get_or_create(
        user=user,
        **{f"{object_type}": obj},
        defaults={'rating': rating_value}
    )

    if not created:
        rating.rating = rating_value
        rating.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_comment(request, object_type, object_id):
    user = request.user
    comment_text = request.POST.get('comment')

    model = {
        'auberge': Auberge,
        'hotel': Hotel,
        'complexe': Complexe
    }.get(object_type)

    if not model:
        # Handle invalid object type
        return redirect('/') # Or to an error page

    obj = get_object_or_404(model, pk=object_id)

    Comment.objects.create(
        user=user,
        **{f"{object_type}": obj},
        comment=comment_text
    )

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_picture(request, object_type, object_id):
    user = request.user
    image = request.FILES.get('image')

    model = {
        'auberge': Auberge,
        'hotel': Hotel,
        'complexe': Complexe
    }.get(object_type)

    if not model:
        # Handle invalid object type
        return redirect('/') # Or to an error page

    obj = get_object_or_404(model, pk=object_id)

    Picture.objects.create(
        user=user,
        **{f"{object_type}": obj},
        image=image
    )

    return redirect(request.META.get('HTTP_REFERER', '/'))


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType  # Add this
from django.contrib.auth.models import Permission  # Add this
from .models import Auberge, Hotel, Complexe, Transport, CustomUser, Resident
from .forms import PropertyAdminAssignmentForm

def is_superuser(user):
    return user.is_superuser

def assign_property_permissions(user, property_type, property_instance):
    content_type = ContentType.objects.get_for_model(property_instance.__class__)

    permission_mapping = {
        'auberge': ['change_auberge', 'view_auberge', 'manage_auberge'],
        'hotel': ['change_hotel', 'view_hotel', 'manage_hotel'],
        'complexe': ['change_complexe', 'view_complexe', 'manage_complexe'],
        'transport': ['change_transport', 'view_transport', 'manage_transport'],
    }

    permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=permission_mapping.get(property_type, [])
    )

    user.user_permissions.add(*permissions)
    user.user_type = f'{property_type}_admin'
    user.save()

@user_passes_test(is_superuser)
def assign_property_admin(request, property_type, property_id):
    model_mapping = {
        'auberge': Auberge,
        'hotel': Hotel,
        'complexe': Complexe,
        'transport': Transport,
    }

    Model = model_mapping.get(property_type)
    if not Model:
        messages.error(request, "Invalid property type")
        return redirect('admin:index')

    property_instance = get_object_or_404(Model, id=property_id)

    if request.method == 'POST':
        form = PropertyAdminAssignmentForm(request.POST, property_type=property_type)
        if form.is_valid():
            admin_user = form.cleaned_data['admin_user']

            # Remove previous admin's permissions if they exist
            if property_instance.owner:
                previous_admin = property_instance.owner
                previous_permissions = previous_admin.user_permissions.filter(
                    content_type=ContentType.objects.get_for_model(property_instance.__class__)
                )
                previous_admin.user_permissions.remove(*previous_permissions)

            # Assign new admin
            property_instance.owner = admin_user
            property_instance.save()

            # Assign permissions to new admin
            assign_property_permissions(admin_user, property_type, property_instance)

            messages.success(request, f"Successfully assigned admin to {property_type}")
            return redirect('admin:index')
    else:
        form = PropertyAdminAssignmentForm(property_type=property_type)

    return render(request, 'admin/assign_property_admin.html', {
        'form': form,
        'property_type': property_type,
        'property_instance': property_instance,
    })



from django.shortcuts import render, get_object_or_404
from .models import Auberge


def auberge_detail(request, auberge_id):
    auberge = get_object_or_404(Auberge, pk=auberge_id)
    form = ReservationForm()  # Initialize the form outside the if block
    context = {
        'auberge': auberge,
        'form': form,
    }
    return render(request, 'core/auberge_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Complexe


def complexe_detail(request, complexe_id):
    complexe = get_object_or_404(Complexe, pk=complexe_id)
    form = ReservationForm()  # Initialize the form outside the if block
    context = {
        'complexe': complexe,
        'form': form,
    }
    return render(request, 'core/complexe_detail.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='core.authentication.BlacklistAuthBackend')
            return redirect('core:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Use 'username' because that's what the form uses
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Check if the user is blacklisted
                try:
                    resident = Resident.objects.get(user=user)
                    if resident.is_blacklisted:
                        form.add_error(None, "This user is blacklisted.")
                        return render(request, 'core/login.html', {'form': form})
                except Resident.DoesNotExist:
                    pass
                login(request, user, backend='core.authentication.BlacklistAuthBackend')
                return redirect('core:index')
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})



@login_required
def make_reservation(request, object_type, object_id):
    model = {
        'auberge': Auberge,
        'hotel': Hotel,
        'complexe': Complexe
    }.get(object_type)

    if not model:
        messages.error(request, "Invalid object type.")
        return redirect('core:index')  # Or to an error page

    obj = get_object_or_404(model, pk=object_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            # Set the appropriate foreign key based on object type
            if object_type == 'hotel':
                reservation.hotel = obj
            elif object_type == 'auberge':
                reservation.auberge = obj
            elif object_type == 'complexe':
                reservation.complexe = obj

            try:
                reservation.save()
                messages.success(request, 'Reservation successful!')
                return redirect(f'core:{object_type}_detail', object_id=obj.id)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
        else:
            messages.error(request, "There was an error in the form. Please check your inputs.")
    else:
        form = ReservationForm()

    context = {
        f'{object_type}': obj,
        'form': form,
    }
    return render(request, f'core/{object_type}_detail.html', context)




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
import os
import json


# Configure Google AI Studio API
genai.configure(api_key='AIzaSyDPPgFFxgwxM9QxWLH6B-vz_EprQE9ClMw')
model = genai.GenerativeModel('gemini-exp-1206')

# Placeholder for hotel data (replace with your actual data source)
hotel_data = {
    "name": "Boumerdes Tourist Guide",
    "location": "Boumerdes, Algeria",
    "events": [
        {"name": "Kabyle Music Festival", "date": "2024-07-15", "price": 1000},
        {"name": "Boumerdes Handicrafts Fair", "date": "2024-07-10", "price": 200},
        {"name": "Summer Beach Volleyball Tournament", "date": "2024-08-05", "price": 0}
    ],
    "nearby_hotels": [
        {"name": "Hotel Sahel", "price": "80"},
        {"name": "Hotel Ville des Roses", "price": "120"},
        {"name": "Boumerdes Beach Hotel", "price": "100"}
    ],
    "tourist_attractions": [
        {"name": "Plage de Boumerdes", "description": "A popular beach known for its clear waters and vibrant atmosphere."},
        {"name": "Boumerdes Waterfront Promenade", "description": "A scenic spot perfect for evening strolls and enjoying the sea breeze."},
        {"name": "Mosquée Al-Takwa", "description": "A beautiful mosque with modern architectural design."},
        {"name": "Institut National de la Météorologie", "description": "Offers insights into Algeria's meteorological studies."}
    ],
    "restaurants": [
        {"name": "La Marina Restaurant", "specialty": "Seafood and Mediterranean cuisine"},
        {"name": "Café Fennec", "specialty": "Traditional Algerian tea and snacks"},
        {"name": "Pizzeria Mediterraneo", "specialty": "Wood-fired pizzas and Italian dishes"}
    ],
    "activities": [
        {"name": "Snorkeling at Plage les Pins", "price": 1500, "description": "Explore the underwater beauty of Boumerdes."},
        {"name": "Hiking in Zemmouri El Bahri", "price": 0, "description": "Enjoy scenic trails and lush greenery."},
        {"name": "Cultural Tour of Boumerdes City Center", "price": 500, "description": "Discover the rich history and culture of Boumerdes."}
    ]
}


def get_llm_suggestions(user_constraint, hotel_data):
    prompt = f"""You are a helpful hotel concierge.

    A guest is staying at our hotel. Here is some information about the hotel and nearby events:

    {json.dumps(hotel_data)}

    The guest has provided the following constraint:

    {user_constraint}

    Please provide some suggestions for the guest based on their constraint and the available events/hotels in the state of boumerdes, algeria
 return a short response that has the essensial information
        """
    response = model.generate_content(prompt)
    return response.text

def chat_view(request):
    return render(request, 'core/chat.html')

def preferences_chat_view(request):
    return render(request, 'core/preferences_chat.html')


def get_suggestions(request):
     if request.method == "POST":
        user_input = request.POST.get("user_input")
        constraint_type = request.POST.get("constraint_type")

        if constraint_type == "time":
            user_constraint = f"Time: {user_input}"
        elif constraint_type == "budget":
            user_constraint = f"Budget: {user_input}"
        else:
             return JsonResponse({"error": "Invalid constraint type"}, status=400)


        suggestions = get_llm_suggestions(user_constraint, hotel_data)
        return JsonResponse({"suggestions": suggestions})

     return JsonResponse({"error":"Invalid Request"}, status=400)