from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Patient URLs
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/add/', views.PatientCreateView.as_view(), name='patient_add'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_edit'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    
    # Doctor URLs
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/add/', views.DoctorCreateView.as_view(), name='doctor_add'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    
    # Appointment URLs
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/book/', views.AppointmentCreateView.as_view(), name='appointment_book'),
    path('appointments/<int:pk>/', views.AppointmentStatusUpdateView.as_view(), name='appointment_update'),
    
    # Prescription URLs
    path('prescriptions/add/<int:appointment_id>/', views.PrescriptionCreateView.as_view(), name='prescription_add'),
    path('prescriptions/patient/<int:patient_id>/', views.PrescriptionHistoryView.as_view(), name='prescription_history'),
    path('prescriptions/<int:pk>/edit/', views.PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', views.PrescriptionDeleteView.as_view(), name='prescription_delete'),
    
    # Billing URLs
    path('billing/generate/<int:appointment_id>/', views.BillCreateView.as_view(), name='bill_generate'),
    path('billing/invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    
    # User Management URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
