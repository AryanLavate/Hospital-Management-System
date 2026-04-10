from django import forms
from .models import Patient, Doctor, Appointment, Prescription, Bill
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave blank to keep current password")

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        help_texts = {
            'is_staff': 'Designates whether the user can log into this admin site.',
            'is_superuser': 'Designates that this user has all permissions without explicitly assigning them.',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'address', 'medical_history']

class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False, help_text="Required for new account")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Required for new account")

    class Meta:
        model = Doctor
        fields = ['user', 'username', 'password', 'specialization', 'phone', 'email', 'schedule']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['user'].help_text = "Select an existing user OR fill in Username/Password below"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not user and (not username or not password):
            raise ValidationError("You must either select an existing user or provide both a username and password for a new account.")
        
        if username and User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
            
        return cleaned_data

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if doctor and date and time:
            if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
                raise ValidationError("This doctor already has an appointment at this time.")
        return cleaned_data

class PresetForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['diagnosis', 'medicines']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['consultation_fee', 'medicine_charges', 'other_charges', 'payment_status']
        widgets = {
            'consultation_fee': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
            'medicine_charges': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
            'other_charges': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
        }
        labels = {
            'consultation_fee': 'Consultation Fee (INR)',
            'medicine_charges': 'Medicine Charges (INR)',
            'other_charges': 'Other Charges (INR)',
        }
