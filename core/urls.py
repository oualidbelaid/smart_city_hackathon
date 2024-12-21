from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('transport/', views.transport, name='transport'),
    path('auberges/', views.auberge_list, name='auberge_list'),
    path('auberges/<int:auberge_id>/', views.auberge_detail, name='auberge_detail'),
    path('complexes/', views.complexe_list, name='complexe_list'),
    path('complexes/<int:complexe_id>/', views.complexe_detail, name='complexe_detail'),
    path('profile/', views.profile, name='profile'),
    path('rate/<str:object_type>/<int:object_id>/', views.rate_object, name='rate_object'),
    path('comment/<str:object_type>/<int:object_id>/', views.add_comment, name='add_comment'),
    path('picture/<str:object_type>/<int:object_id>/', views.add_picture, name='add_picture'),
    path('assign-admin/<str:property_type>/<int:property_id>/', views.assign_property_admin, name='assign_property_admin'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:index'), name='logout'),

    # New path for making reservations
    path('reserve/<str:object_type>/<int:object_id>/', views.make_reservation, name='make_reservation'),
    path('chat/', views.chat_view, name='chat'),
    path('preferences_chat/', views.preferences_chat_view, name='preferences_chat'),
    path('get_suggestions/', views.get_suggestions, name='get_suggestions'),
]