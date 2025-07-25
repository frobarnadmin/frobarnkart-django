from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Account, UserProfile, Tailor

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_tailor', 'is_active')
    list_display_links = ('email','first_name','last_name')
    list_editable = ('is_tailor',)
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" height="30" style="border-radius:30%"/>'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile picture'
    list_display = ('thumbnail','user', 'city', 'state', 'country')
    list_filter = ('state', 'country')

class TailorAdmin(admin.ModelAdmin):
    list_display = ('account', 'business_name', 'business_city', 'created_at')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tailor, TailorAdmin)
