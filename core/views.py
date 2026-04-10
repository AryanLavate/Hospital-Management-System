from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Patient, Doctor, Appointment, Prescription, Bill
from .forms import PatientForm, DoctorForm, AppointmentForm, PresetForm, BillForm, UserForm
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.utils import timezone

class LandingView(TemplateView):
    template_name = 'core/landing.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Analytics for Admin
        today = timezone.localdate()
        
        if self.request.user.is_superuser:
            context['total_patients'] = Patient.objects.count()
            context['total_doctors'] = Doctor.objects.count()
            context['total_appointments'] = Appointment.objects.count()
            total_revenue = Bill.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            context['total_revenue'] = total_revenue
            context['has_revenue'] = total_revenue > 0

            # Aggregate revenue per patient for dashboard list
            patient_revenue = (
                Bill.objects.values('patient__id', 'patient__name')
                .annotate(total_paid=Sum('total_amount'))
                .order_by('-total_paid')
            )
            context['patient_revenue'] = patient_revenue
        
        if hasattr(self.request.user, 'doctor_profile'):
            context['today_appointments'] = Appointment.objects.filter(
                doctor=self.request.user.doctor_profile,
                date=today
            ).order_by('time')
        else:
            # For Receptionists (Admins are also treated as staff here)
            context['today_all_appointments'] = Appointment.objects.filter(date=today).order_by('time')

        # Simple activity log derived from latest objects
        recent_patient = Patient.objects.order_by('-created_at').first()
        recent_appointment = Appointment.objects.order_by('-created_at').first()
        recent_bill = Bill.objects.order_by('-created_at').first()
        context['recent_patient'] = recent_patient
        context['recent_appointment'] = recent_appointment
        context['recent_bill'] = recent_bill
            
        return context

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'core/patients/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Patient.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query))
        return Patient.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_doctor'] = hasattr(self.request.user, 'doctor_profile')
        return context

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'core/patients/patient_detail.html'
    context_object_name = 'patient'

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'core/patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'core/doctors/doctor_list.html'
    context_object_name = 'doctors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_doctor'] = hasattr(self.request.user, 'doctor_profile')
        return context

class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        if not user:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True # Allow them to log in to the system
            user.save()
            form.instance.user = user
        
        return super().form_valid(form)

class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Doctor
    template_name = 'core/doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

    def test_func(self):
        return self.request.user.is_superuser

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'core/appointments/appointment_list.html'
    context_object_name = 'appointments'

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'core/appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')

class AppointmentStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['status']
    template_name = 'core/appointments/appointment_update.html'
    success_url = reverse_lazy('appointment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.object
        return context

class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    form_class = PresetForm
    template_name = 'core/prescriptions/prescription_form.html'

    def dispatch(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get('appointment_id')
        existing_prescription = Prescription.objects.filter(appointment_id=appointment_id).first()
        if existing_prescription:
            return redirect('prescription_update', pk=existing_prescription.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_id'])
        form.instance.doctor = self.request.user.doctor_profile
        form.instance.appointment = appointment
        form.instance.patient = appointment.patient
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = get_object_or_404(Appointment, pk=self.kwargs['appointment_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('appointment_list')

class PrescriptionHistoryView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'core/prescriptions/prescription_history.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        return Prescription.objects.filter(patient_id=self.kwargs['patient_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        context['patient'] = patient
        return context

class PrescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = PresetForm
    template_name = 'core/prescriptions/prescription_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.object.appointment
        return context

    def get_success_url(self):
        return reverse_lazy('prescription_history', kwargs={'patient_id': self.object.patient_id})

class PrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prescription
    template_name = 'core/prescriptions/prescription_confirm_delete.html'

    def get_success_url(self):
        patient_id = self.object.patient_id
        return reverse_lazy('prescription_history', kwargs={'patient_id': patient_id})

class BillCreateView(LoginRequiredMixin, CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'core/billing/bill_form.html'

    def dispatch(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get('appointment_id')
        existing_bill = Bill.objects.filter(appointment_id=appointment_id).first()
        if existing_bill:
            return redirect('invoice_detail', pk=existing_bill.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_id'])
        form.instance.appointment = appointment
        form.instance.patient = appointment.patient
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('invoice_detail', kwargs={'pk': self.object.pk})

class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = 'core/billing/invoice_detail.html'

# User Management Views (Superuser only)
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'core/users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'core/users/user_form.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'core/users/user_form.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'core/users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser
    
    def delete(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if user_to_delete == request.user:
            from django.contrib import messages
            messages.error(request, "You cannot delete your own account.")
            return redirect('user_list')
        return super().delete(request, *args, **kwargs)
