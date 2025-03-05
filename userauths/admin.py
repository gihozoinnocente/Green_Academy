from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'full_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'full_name']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date']
    search_fields = ['full_name', 'user__username', 'user__email']
    list_filter = ['user__role']

# Register models with custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)