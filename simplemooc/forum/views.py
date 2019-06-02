from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView, View

from .forms import ReplyForm
from .models import Reply, Thread


class ForumView(ListView):

    context_object_name = 'threads'
    paginate_by = 1
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')
        if order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'comments':
            queryset = queryset.order_by('-answers')
        tag = self.kwargs.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context


class ThreadView(DetailView):

    model = Thread
    context_object_name = 'thread'
    template_name = 'forum/thread.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.success(
                self.request, 'Você precisa estar logado para responder no tópico!'
            )
            return redirect(self.request.path)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'Resposta enviada!')
        context['form'] = ReplyForm()
        return self.render_to_response(context)


class ReplyCorrectView(View):

    correct = True

    def get(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, thread__author=request.user)
        reply.correct = self.correct
        reply.save()
        if self.correct:
            messages.success(request, 'Resposta marcada com sucesso!')
        else:
            messages.success(request, 'Resposta desmarcada com sucesso!')
        return redirect(reply.thread.get_absolute_url())
