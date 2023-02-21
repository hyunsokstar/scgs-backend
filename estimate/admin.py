from django.contrib import admin
from .models import Estimate


@admin.register(Estimate)
class Booking(admin.ModelAdmin):
    list_display = (
        "title",
        "product",
        "manager",
        "email",
        "phone_number",
        "content",
        "estimate_require_completion",
        "memo",
    )