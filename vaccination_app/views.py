from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q

from .models import UserProfile, Child, Vaccine, VaccinationRecord, Appointment
from .forms import (
    CustomLoginForm, RegisterForm, ChildForm,
    AppointmentForm, VaccinationRecordForm, VaccineForm
)


def get_user_role(user):
    try:
        return user.profile.role
    except UserProfile.DoesNotExist:
        return 'parent'


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'vaccination_app/login.html', {'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('dashboard')
    return render(request, 'vaccination_app/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    role = get_user_role(request.user)
    today = timezone.now().date()
    context = {'role': role, 'today': today}

    if role == 'admin' or request.user.is_superuser:
        context['total_children'] = Child.objects.count()
        context['total_parents'] = UserProfile.objects.filter(role='parent').count()
        context['total_doctors'] = UserProfile.objects.filter(role='doctor').count()
        context['upcoming_appointments'] = Appointment.objects.filter(
            appointment_date__gte=today, status__in=['pending', 'confirmed']
        ).order_by('appointment_date')[:5]
        context['overdue_vaccinations'] = VaccinationRecord.objects.filter(
            scheduled_date__lt=today, status='scheduled'
        ).count()
        context['recent_records'] = VaccinationRecord.objects.filter(
            status='completed'
        ).order_by('-administered_date')[:5]

    elif role == 'doctor':
        context['my_appointments'] = Appointment.objects.filter(
            doctor=request.user, appointment_date__gte=today
        ).order_by('appointment_date')[:5]
        context['today_appointments'] = Appointment.objects.filter(
            doctor=request.user, appointment_date=today
        )
        context['recent_records'] = VaccinationRecord.objects.filter(
            doctor=request.user
        ).order_by('-administered_date')[:5]

    else:  # parent
        children = Child.objects.filter(parent=request.user)
        context['children'] = children
        context['upcoming_appointments'] = Appointment.objects.filter(
            parent=request.user, appointment_date__gte=today,
            status__in=['pending', 'confirmed']
        ).order_by('appointment_date')[:5]
        context['upcoming_vaccinations'] = VaccinationRecord.objects.filter(
            child__parent=request.user,
            scheduled_date__gte=today,
            status='scheduled'
        ).order_by('scheduled_date')[:5]
        context['overdue_count'] = VaccinationRecord.objects.filter(
            child__parent=request.user,
            scheduled_date__lt=today,
            status='scheduled'
        ).count()

    return render(request, 'vaccination_app/dashboard.html', context)


# ─── CHILDREN ───────────────────────────────────────────────
@login_required
def children_list(request):
    role = get_user_role(request.user)
    if role in ['admin', 'doctor'] or request.user.is_superuser:
        children = Child.objects.select_related('parent').all()
    else:
        children = Child.objects.filter(parent=request.user)
    return render(request, 'vaccination_app/children_list.html', {'children': children, 'role': role})


@login_required
def child_detail(request, pk):
    child = get_object_or_404(Child, pk=pk)
    role = get_user_role(request.user)
    if role == 'parent' and child.parent != request.user:
        messages.error(request, 'Access denied.')
        return redirect('children_list')
    records = VaccinationRecord.objects.filter(child=child).select_related('vaccine')
    appointments = Appointment.objects.filter(child=child)
    return render(request, 'vaccination_app/child_detail.html', {
        'child': child, 'records': records, 'appointments': appointments, 'role': role
    })


@login_required
def child_add(request):
    form = ChildForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        child = form.save(commit=False)
        child.parent = request.user
        child.save()
        messages.success(request, f'{child.first_name} added successfully!')
        return redirect('children_list')
    return render(request, 'vaccination_app/child_form.html', {'form': form, 'title': 'Add Child'})


@login_required
def child_edit(request, pk):
    child = get_object_or_404(Child, pk=pk)
    form = ChildForm(request.POST or None, instance=child)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Updated successfully!')
        return redirect('child_detail', pk=pk)
    return render(request, 'vaccination_app/child_form.html', {'form': form, 'title': 'Edit Child'})


@login_required
def child_delete(request, pk):
    child = get_object_or_404(Child, pk=pk)
    if request.method == 'POST':
        child.delete()
        messages.success(request, 'Child record deleted.')
        return redirect('children_list')
    return render(request, 'vaccination_app/confirm_delete.html', {'object': child})


# ─── APPOINTMENTS ────────────────────────────────────────────
@login_required
def appointments_list(request):
    role = get_user_role(request.user)
    if role in ['admin'] or request.user.is_superuser:
        appointments = Appointment.objects.select_related('child', 'parent', 'doctor').all()
    elif role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.filter(parent=request.user)
    return render(request, 'vaccination_app/appointments_list.html', {
        'appointments': appointments, 'role': role
    })


@login_required
def appointment_add(request):
    form = AppointmentForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appt = form.save(commit=False)
        appt.parent = request.user
        appt.save()
        form.save_m2m()
        messages.success(request, 'Appointment scheduled!')
        return redirect('appointments_list')
    return render(request, 'vaccination_app/appointment_form.html', {'form': form, 'title': 'Schedule Appointment'})


@login_required
def appointment_update_status(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'confirmed', 'completed', 'cancelled']:
            appt.status = status
            appt.save()
            messages.success(request, 'Appointment status updated.')
    return redirect('appointments_list')


# ─── VACCINATION RECORDS ─────────────────────────────────────
@login_required
def records_list(request):
    role = get_user_role(request.user)
    if role in ['admin', 'doctor'] or request.user.is_superuser:
        records = VaccinationRecord.objects.select_related('child', 'vaccine', 'doctor').all()
    else:
        records = VaccinationRecord.objects.filter(child__parent=request.user)
    return render(request, 'vaccination_app/records_list.html', {'records': records, 'role': role})


@login_required
def record_add(request):
    role = get_user_role(request.user)
    form = VaccinationRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        if role == 'doctor':
            record.doctor = request.user
        record.save()
        messages.success(request, 'Vaccination record saved!')
        return redirect('records_list')
    return render(request, 'vaccination_app/record_form.html', {'form': form, 'title': 'Add Record'})


@login_required
def record_edit(request, pk):
    record = get_object_or_404(VaccinationRecord, pk=pk)
    form = VaccinationRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Record updated!')
        return redirect('records_list')
    return render(request, 'vaccination_app/record_form.html', {'form': form, 'title': 'Edit Record'})


# ─── VACCINES ────────────────────────────────────────────────
@login_required
def vaccines_list(request):
    vaccines = Vaccine.objects.all()
    return render(request, 'vaccination_app/vaccines_list.html', {'vaccines': vaccines})


@login_required
def vaccine_add(request):
    role = get_user_role(request.user)
    if role not in ['admin', 'doctor'] and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('vaccines_list')
    form = VaccineForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vaccine added!')
        return redirect('vaccines_list')
    return render(request, 'vaccination_app/vaccine_form.html', {'form': form, 'title': 'Add Vaccine'})


# ─── USERS (Admin) ────────────────────────────────────────────
@login_required
def users_list(request):
    if not request.user.is_superuser and get_user_role(request.user) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('dashboard')
    users = User.objects.select_related('profile').all()
    return render(request, 'vaccination_app/users_list.html', {'users': users})


def create_user(request):
    if not request.user.is_superuser and get_user_role(request.user) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User created successfully!')
        return redirect('users_list')
    return render(request, 'vaccination_app/child_form.html', {'form': form, 'title': 'Create New User'})
