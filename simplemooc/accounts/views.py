from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditAccountForm, PasswordResetForm, RegisterForm
from .models import PasswordReset
from simplemooc.courses.models import Enrollment


User = get_user_model()


@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    enrollments = Enrollment.objects.filter(user=request.user)
    context = {
        'enrollments': enrollments
    }
    return render(request, template_name, context)


def register(request):
    template_name = 'accounts/register.html'
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user = authenticate(username=user.username,
                            password=form.cleaned_data['password1'])
        login(request, user)
        return redirect('core:home')
    context = {'form': form}
    return render(request, template_name, context)


def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key, confirmed=False)
    if reset.key_has_expired():
        messages.error(
            request, 'Seu link de recuperação de senha expirou. '
            'Informe seu e-mail para receber um novo.'
        )
        return redirect('accounts:password_reset')
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        reset.confirm()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    form = EditAccountForm(instance=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Os dados da sua conta foram alterados com sucesso!')
        return redirect('accounts:dashboard')
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)
