from django import forms
from django.conf import settings

from .models import Comment
from simplemooc.core.mail import send_mail_template


class ContactCourse(forms.Form):

    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

    def send_mail(self, course):
        subject = f'{course} - Contato'
        template_name = 'courses/contact_email.html'
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
