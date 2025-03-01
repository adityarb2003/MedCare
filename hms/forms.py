from django import forms
from .models import Appointment, Patient, Doctor,MedicalRecord
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PatientRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    address = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DoctorRegistrationForm(UserCreationForm):
    specialty = forms.CharField(max_length=100)
    license_number = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        doctor = Doctor.objects.create(user=user, specialty=self.cleaned_data['specialty'],
                                       license_number=self.cleaned_data['license_number'])

        return user

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'diagnosis', 'prescription']
        widgets = {
            'diagnosis':forms.Textarea(attrs={'rows':4}),
            'prescription':forms.Textarea(attrs={'rows':4}),
        }

