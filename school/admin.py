from django.contrib import admin
from .models import School, UserProfile

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')
