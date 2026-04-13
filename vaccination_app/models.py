from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('parent', 'Parent/Guardian'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class Child(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="in kg")
    allergies = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age_in_months(self):
        today = timezone.now().date()
        delta = today - self.date_of_birth
        return delta.days // 30

    @property
    def age_display(self):
        months = self.age_in_months
        if months < 12:
            return f"{months} months"
        years = months // 12
        rem = months % 12
        return f"{years}y {rem}m" if rem else f"{years} years"


class Vaccine(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    recommended_age_months = models.PositiveIntegerField(help_text="Recommended age in months")
    doses_required = models.PositiveIntegerField(default=1)
    interval_days = models.PositiveIntegerField(default=0, help_text="Days between doses (0 if single dose)")
    manufacturer = models.CharField(max_length=200, blank=True)
    is_mandatory = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class VaccinationRecord(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='administered_vaccines')
    dose_number = models.PositiveIntegerField(default=1)
    scheduled_date = models.DateField()
    administered_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    batch_number = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=100, blank=True, help_text="e.g., Left arm, Right thigh")
    notes = models.TextField(blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']
        unique_together = ['child', 'vaccine', 'dose_number']

    def __str__(self):
        return f"{self.child} - {self.vaccine.short_name} (Dose {self.dose_number})"

    @property
    def is_overdue(self):
        return self.status == 'scheduled' and self.scheduled_date < timezone.now().date()


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='appointments')
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    vaccines = models.ManyToManyField(Vaccine, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.child} - {self.appointment_date} at {self.appointment_time}"
