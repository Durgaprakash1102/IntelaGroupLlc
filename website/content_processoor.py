from django.conf import settings


def layout_template(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {
            "layout_template": "includes/sidebar.html"
        }

    return {
        "layout_template": "base.html"
    }