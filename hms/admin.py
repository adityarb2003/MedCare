# from django.contrib import admin
# from .models import Patient,Doctor,Appointment,MedicalRecord
#
# # Register your models here.
# @admin.register(Patient)
# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('get_full_name','date_of_birth','phone_number')
#     search_fields = ('user__first_name', 'user__last_name', 'phone_number')
#
#     def get_full_name(self,obj):
#         return obj.user.get_full_name()
#     get_full_name.short_description = 'Full Name'
#
# @admin.register(Doctor)
# class DoctorAdmin(admin.ModelAdmin):
#     list_display = ('get_full_name', 'specialty', 'license_number')
#     search_fields = ('user__first_name', 'user__last_name', 'specialty', 'license_number')
#
#     def get_full_name(self, obj):
#         return f"Dr. {obj.user.get_full_name()}"
#     get_full_name.short_description = 'Full Name'
#
# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('patient','doctor','date_time','reason')
#     list_filter = ('doctor','date_time')
#     search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__last_name')
#
# @admin.register(MedicalRecord)
# class MedicalRecordAdmin(admin.ModelAdmin):
#     list_display = ('patient','doctor','date','diagnosis')
#     list_filter = ('doctor','date')
#     search_fields = ('patient__user__first_name', 'patient__user__last_name', 'diagnosis')


from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, Doctor, Appointment, MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('date_of_birth',)

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Name'

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'license_number')
    search_fields = ('user__first_name', 'user__last_name', 'specialty')
    list_filter = ('specialty',)

    def full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    full_name.short_description = 'Name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time', 'reason', 'status_colored')
    list_filter = ('status', 'date_time', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__last_name')
    date_hierarchy = 'date_time'

    def status_colored(self, obj):
        colors = {
            'P': 'orange',
            'A': 'green',
            'D': 'red',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors[obj.status],
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'diagnosis_summary')
    list_filter = ('date', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__last_name', 'diagnosis')
    date_hierarchy = 'date'

    def diagnosis_summary(self, obj):
        return obj.diagnosis[:50] + '...' if len(obj.diagnosis) > 50 else obj.diagnosis
    diagnosis_summary.short_description = 'Diagnosis'