from django.contrib import admin
from .models import Contact, NewsletterContact

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "message")
    list_filter = ("created_at",)

@admin.register(NewsletterContact)
class NewsletterContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'source', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
