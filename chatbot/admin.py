from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['is_user', 'content', 'created_at']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'message_count', 'created_at']
    list_filter = ['created_at']
    inlines = [ChatMessageInline]
    readonly_fields = ['session_id', 'message_count', 'created_at']
