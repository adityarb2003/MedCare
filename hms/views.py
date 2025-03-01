from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Doctor, Appointment, MedicalRecord, Patient
from .forms import AppointmentForm, PatientRegistrationForm, DoctorRegistrationForm, MedicalRecordForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'patient'):
            return redirect('patient_dashboard')
        elif hasattr(request.user, 'doctor'):
            return redirect('doctor_dashboard')
        elif request.user.is_staff:
            return redirect('admin:index')
    return render(request, 'hms/home.html')


@login_required
def user_redirect(request):
    if request.user.is_staff:
        return redirect('admin:index')
    elif hasattr(request.user, 'patient'):
        return redirect('patient_dashboard')
    elif hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')
    else:
        return redirect('home')


class DoctorListView(ListView):
    model = Doctor
    template_name = 'hms/doctor_list.html'
    context_object_name = 'doctors'


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'hms/doctor_detail.html'
    context_object_name = 'doctor'


@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    return render(request, 'hms/appointment_form.html', {'form': form})


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'hms/appointment_detail.html'
    context_object_name = 'appointment'


@method_decorator(login_required, name='dispatch')
class PatientDashboardView(ListView):
    template_name = 'hms/patient_dashboard.html'
    context_object_name = 'appointments'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'patient'):
            return redirect('user_redirect')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.patient).order_by('date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_records'] = MedicalRecord.objects.filter(patient=self.request.user.patient).order_by('-date')
        return context




# @method_decorator(login_required, name='dispatch')
# class DoctorDashboardView(ListView):
#     template_name = 'hms/doctor_dashboard.html'
#     context_object_name = 'appointments'
#
#     def dispatch(self, request, *args, **kwargs):
#         if not hasattr(request.user, 'doctor'):
#             return redirect('user_redirect')
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_queryset(self):
#         return Appointment.objects.filter(doctor=self.request.user.doctor).order_by('date_time')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['patients'] = Patient.objects.filter(appointment__doctor=self.request.user.doctor).distinct()
#         context['recent_records'] = MedicalRecord.objects.filter(doctor=self.request.user.doctor).order_by('-date')[:5]
#         return context


def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
            )
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'hms/register_patient.html', {'form': form})


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            # Process form data
            specialty = form.cleaned_data['specialty']
            doctor = form.save(commit=False)
            doctor.specialty = specialty
            doctor.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'hms/register_doctor.html', {'form': form})


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'hms/medical_record_detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        if hasattr(self.request.user, 'patient'):
            return MedicalRecord.objects.filter(patient=self.request.user.patient)
        elif hasattr(self.request.user, 'doctor'):
            return MedicalRecord.objects.all()
        return MedicalRecord.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PatientMedicalHistoryView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'hms/patient_medical_history.html'
    context_object_name = 'records'

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        if hasattr(self.request.user, 'doctor') or self.request.user == patient.user:
            return MedicalRecord.objects.filter(patient=patient).order_by('-date')

        return MedicalRecord.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['pk'])
        return context


@login_required
def add_medical_record(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Only doctors can add medical records.")
        return redirect('user_redirect')

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.doctor = request.user.doctor
            medical_record.save()
            messages.success(request, "Medical record added successfully.")
            return redirect('doctor_dashboard')
    else:
        form = MedicalRecordForm()

    return render(request, 'hms/medical_record_form.html', {'form': form})


@login_required
def update_medical_record(request, pk):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Only doctors can update medical records.")
        return redirect('user_redirect')

    medical_record = get_object_or_404(MedicalRecord, pk=pk)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Medical record updated successfully.")
            return redirect('doctor_dashboard')
    else:
        form = MedicalRecordForm(instance=medical_record)

    return render(request, 'hms/medical_record_form.html', {'form': form})


@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if the logged-in user is the doctor for this appointment
    if request.user.doctor != appointment.doctor:
        messages.error(request, "You don't have permission to approve this appointment.")
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            appointment.status = Appointment.APPROVED
            messages.success(request, "Appointment approved successfully.")
        elif action == 'decline':
            appointment.status = Appointment.DECLINED
            messages.success(request, "Appointment declined successfully.")
        appointment.save()

    return redirect('doctor_dashboard')


class DoctorDashboardView(ListView):
    template_name = 'hms/doctor_dashboard.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user.doctor).order_by('date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_appointments'] = self.get_queryset().filter(status=Appointment.PENDING)
        context['recent_records'] = MedicalRecord.objects.filter(doctor=self.request.user.doctor).order_by('-date')[:5]
        context['patients'] = Patient.objects.filter(appointment__doctor=self.request.user.doctor).distinct()
        return context



