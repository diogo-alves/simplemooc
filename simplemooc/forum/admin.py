from django.contrib import admin

from .models import Thread, Reply


class ThreadAdmin(admin.ModelAdmin):

    list_display = ['title', 'body', 'author', 'updated_at']
    search_fields = ['title', 'body', 'author__username']
    prepopulated_fields = {'slug': ('title',)}


class ReplyAdmin(admin.ModelAdmin):

    list_display = ['thread', 'reply', 'author', 'correct', 'updated_at']
    search_fields = ['thread', 'reply', 'author__username']
    list_filter = ['thread__title', 'author__username']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
