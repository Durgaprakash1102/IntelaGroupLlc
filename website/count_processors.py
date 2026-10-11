from .models import (
    ContactMessage,
    CareerApplicant,
    CandidateSubmission,
)


def admin_review_counts(request):

    # Do not run these queries for logged-out users.
    if not request.user.is_authenticated:
        return {
            "new_contacts_count": 0,
            "pending_career_applicants_count": 0,
            "new_candidates_count": 0,
            "total_review_count": 0,
        }

    new_contacts_count = (
        ContactMessage.objects
        .filter(status=ContactMessage.NEW)
        .count()
    )

    pending_career_applicants_count = (
        CareerApplicant.objects
        .filter(status=CareerApplicant.APPLIED)
        .count()
    )

    new_candidates_count = (
        CandidateSubmission.objects
        .filter(status=CandidateSubmission.NEW)
        .count()
    )

    total_review_count = (
        new_contacts_count
        + pending_career_applicants_count
        + new_candidates_count
    )

    return {
        "new_contacts_count": new_contacts_count,
        "pending_career_applicants_count": pending_career_applicants_count,
        "new_candidates_count": new_candidates_count,
        "total_review_count": total_review_count,
    }