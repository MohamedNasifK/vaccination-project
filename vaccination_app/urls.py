from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Children
    path('children/', views.children_list, name='children_list'),
    path('children/add/', views.child_add, name='child_add'),
    path('children/<int:pk>/', views.child_detail, name='child_detail'),
    path('children/<int:pk>/edit/', views.child_edit, name='child_edit'),
    path('children/<int:pk>/delete/', views.child_delete, name='child_delete'),

    # Appointments
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/add/', views.appointment_add, name='appointment_add'),
    path('appointments/<int:pk>/status/', views.appointment_update_status, name='appointment_update_status'),

    # Vaccination Records
    path('records/', views.records_list, name='records_list'),
    path('records/add/', views.record_add, name='record_add'),
    path('records/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('records/<int:pk>/reminder/', views.send_reminder, name='send_reminder'),

    # Vaccines
    path('vaccines/', views.vaccines_list, name='vaccines_list'),
    path('vaccines/add/', views.vaccine_add, name='vaccine_add'),

    # Users (Admin)
    path('users/', views.users_list, name='users_list'),
]
