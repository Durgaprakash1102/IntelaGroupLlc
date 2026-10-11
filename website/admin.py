from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
    )

    search_fields = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )

    ordering = (
        "-date_joined",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Intela Group",
            {
                "fields": (
                    "phone_number",
                    "role",
                    "email_verified",
                    "otp",
                    "otp_created_at",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Intela Group",
            {
                "fields": (
                    "email",
                    "phone_number",
                    "role",
                )
            },
        ),
    )


from django.contrib import admin
from .models import Partner, ClientTestimonial


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "website_url",
        "is_active",
        "display_order",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active", "display_order")
    ordering = ("display_order", "name")


@admin.register(ClientTestimonial)
class ClientTestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "company_name",
        "designation",
        "rating",
        "is_active",
        "display_order",
    )
    list_filter = ("is_active", "rating")
    search_fields = (
        "client_name",
        "company_name",
        "designation",
        "testimonial",
    )
    list_editable = ("is_active", "display_order")
    ordering = ("display_order", "-created_at")
