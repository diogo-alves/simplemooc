from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from simplemooc.core.mail import send_mail_template


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )


class Course(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    start_date = models.DateField('Data de início', null=True, blank=True)
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )
    created_at = models.DateTimeField('Criado em:', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em:', auto_now=True)

    objects = CourseManager()

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:details', args=[self.slug])

    def released_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__lte=today)


class Lesson(models.Model):

    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='lessons',
        on_delete=models.CASCADE
    )
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'courses:lesson', args=[self.course.slug, self.pk]
        )

    def is_available(self):
        today = timezone.now().date()
        return today >= self.release_date


class Material(models.Model):

    lesson = models.ForeignKey(
        Lesson, verbose_name='Aula', related_name='materials',
        on_delete=models.CASCADE
    )
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo incorporado', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'courses:material', args=[self.lesson.course.slug, self.pk]
        )

    def is_embedded(self):
        return bool(self.embedded)


class Enrollment(models.Model):

    PENDING, APPROVED, CANCELED = (0, 1, 2)
    STATUS_CHOICES = (
        (PENDING, 'Pendente'),
        (APPROVED, 'Aprovado'),
        (CANCELED, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='enrollments', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments',
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=PENDING, blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:

        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)

    def active(self):
        self.status = self.APPROVED
        self.save()

    def is_approved(self):
        return self.status == self.APPROVED


class Announcement(models.Model):

    course = models.ForeignKey(
        Course, verbose_name='Curso',
        related_name='announcements', on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'courses:announcement', args=[self.course.slug, self.pk]
        )


def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        template_name = 'courses/announcement_mail.html'
        context = {'announcement': instance}

        enrollments = Enrollment.objects.filter(course=instance.course, status=1)
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
    post_save_announcement, sender=Announcement,
    dispatch_uid='post_save_announcement'
)


class Comment(models.Model):

    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio',
        related_name='comments', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        on_delete=models.SET_DEFAULT, default='Usuário deletado'
    )
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

    def __str__(self):
        return self.comment
