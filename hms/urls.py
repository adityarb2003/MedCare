from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('user-redirect/', views.user_redirect, name='user_redirect'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('appointment/new/',views.create_appointment,name='create_appointment'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('patient/dashboard/',views.PatientDashboardView.as_view(),name='patient_dashboard'),
    path('doctor/dashboard/',views.DoctorDashboardView.as_view(),name='doctor_dashboard'),
    path('register/patient/',views.register_patient,name='register_patient'),
    path('register/doctor/',views.register_doctor,name='register_doctor'),

    path('medical-record/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('patient/<int:pk>/medical-history/',views.PatientMedicalHistoryView.as_view(), name='patient_medical_history'),

    path('medical-record/add/', views.add_medical_record, name='add_medical_record'),
    path('medical-record/<int:pk>/update/', views.update_medical_record, name='update_medical_record'),
    path('appointment/<int:appointment_id>/approve/', views.approve_appointment, name='approve_appointment'),


]
