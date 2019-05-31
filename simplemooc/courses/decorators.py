from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Course, Enrollment


def enrollment_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        course = get_object_or_404(Course, slug=slug)
        has_permission = request.user.is_staff
        try:
            enrollment = Enrollment.objects.get(
                user=request.user, course=course
            )
        except Enrollment.DoesNotExist:
            message = 'Desculpe. Vocẽ não tem permissão para acessar esta página'
        else:
            if not enrollment.is_approved():
                message = 'Sua inscrição no curso ainda está pendente.'
            has_permission = has_permission or enrollment.is_approved()
        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:dashboard')
        request.course = course
        return view_func(request, *args, **kwargs)
    return _wrapper
