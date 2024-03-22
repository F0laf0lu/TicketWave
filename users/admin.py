from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, Organizer, Attendee


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'is_verified', "user_type", "is_staff", "is_active", "id"]
    list_filter = ["user_type", "is_staff", "is_active"]

    fieldsets = (
        ('Required', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Type', {'fields': ('user_type','is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


    # Fieldsets to show when adding newuser
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","user_type","password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )

    search_fields = ['email', 'first_name', 'last_name', 'user_type']
    ordering = ['email'] 


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    model = Organizer
    list_display = ['user', 'name', 'website', 'contact_phone',"id"] 
    search_fields = ['user', 'name']
    ordering = ['user', 'name']

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    model = Attendee
    list_display = ['user', 'date_of_birth', "id"] 
    search_fields = ['user']
    ordering = ['user']
