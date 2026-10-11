from .models import CompanyDetails


def company_details(request):
    details = (
        CompanyDetails.objects
        .prefetch_related("locations")
        .first()
    )

    return {
        "company_details": details
    }