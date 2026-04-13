from django.contrib import admin
from .models import UserProfile, Child, Vaccine, VaccinationRecord, Appointment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'gender', 'parent']
    list_filter = ['gender', 'blood_group']
    search_fields = ['first_name', 'last_name', 'parent__username']


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'recommended_age_months', 'doses_required', 'is_mandatory']
    list_filter = ['is_mandatory']
    search_fields = ['name', 'short_name']


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['child', 'vaccine', 'dose_number', 'scheduled_date', 'status', 'administered_date']
    list_filter = ['status', 'vaccine']
    search_fields = ['child__first_name', 'child__last_name', 'vaccine__name']
    date_hierarchy = 'scheduled_date'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['child', 'parent', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status']
    search_fields = ['child__first_name', 'parent__username']
    date_hierarchy = 'appointment_date'
