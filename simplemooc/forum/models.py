from django.conf import settings
from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager


class Thread(models.Model):

    title = models.CharField('Título', max_length=100)
    body = models.TextField('Mensagem')
    slug = models.SlugField('Identificador (slug)', unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads',
        on_delete=models.CASCADE
    )
    views = models.PositiveIntegerField('Visualizações', blank=True, default=0)
    answers = models.PositiveIntegerField('Respostas', blank=True, default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)
    tags = TaggableManager()

    class Meta:

        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread', args=[self.slug])


class Reply(models.Model):

    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='author_replies',
        on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        Thread, verbose_name='Tópico', related_name='replies', on_delete=models.CASCADE
    )
    correct = models.BooleanField('Correta?', blank=True, default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:

        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created_at']

    def __str__(self):
        return self.reply[:100]


def post_save_reply(created, instance, **kwargs):
        instance.thread.answers = instance.thread.replies.count()
        instance.thread.save()
        if instance.correct:
            instance.thread.replies.exclude(pk=instance.pk).update(
                correct=False
            )


def post_delete_reply(instance, **kwargs):
        instance.thread.answers = instance.thread.replies.count()
        instance.thread.save()


models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)

models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)
