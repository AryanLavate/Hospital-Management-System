def user_roles(request):
    """
    Adds role-based flags to the template context.
    """
    if request.user.is_authenticated:
        return {
            'is_doctor': hasattr(request.user, 'doctor_profile'),
            'is_receptionist': not request.user.is_superuser and not hasattr(request.user, 'doctor_profile'),
        }
    return {}
