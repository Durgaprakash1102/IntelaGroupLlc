from .models import Service


def navigation_services(request):
    return {
        "navigation_services": Service.objects.filter(
            is_active=True
        ).order_by("title")
    }