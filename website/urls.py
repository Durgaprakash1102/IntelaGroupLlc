from django.urls import path

from . import views


app_name = "website"


urlpatterns = [

    # ========================================================
    # PUBLIC
    # ========================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),
    path(
        "industries/",
        views.industries,
        name="industries"
    ),

    path(
        "services/",
        views.services,
        name="services"
    ),
     path(
        "services/<int:pk>/",
        views.service_detail,
        name="service_detail"
    ),

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        "superuser/signup/",
        views.superuser_signup,
        name="superuser_signup"
    ),

    path(
        "admin/signup/",
        views.admin_signup,
        name="admin_signup"
    ),

    path(
        "admin/signup/verify/",
        views.verify_registration_otp,
        name="verify_registration_otp"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "login/verify/",
        views.verify_login_otp,
        name="verify_login_otp"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path(
        "forgot-password/verify/",
        views.verify_password_otp,
        name="verify_password_otp"
    ),

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),


    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # ========================================================
    # USER MANAGEMENT
    # ========================================================

    path(
        "users/",
        views.users_list,
        name="users_list"
    ),

    path(
        "users/create-admin-hr/",
        views.create_admin_hr,
        name="create_admin_hr"
    ),

    path(
        "users/<int:user_id>/toggle-status/",
        views.toggle_user_status,
        name="toggle_user_status"
    ),


    # ========================================================
    # SERVICE MANAGEMENT
    # ========================================================

    path(
        "dashboard/services/",
        views.manage_services,
        name="manage_services"
    ),

    path(
        "dashboard/services/delete/<int:service_id>/",
        views.delete_service,
        name="delete_service"
    ),

    path(
        "dashboard/services/toggle/<int:service_id>/",
        views.toggle_service_status,
        name="toggle_service_status"
    ),
    path(
    "dashboard/company-contact/",
    views.manage_company_contact,
    name="manage_company_contact"
),path(
    "contact/",
    views.contact,
    name="contact"
),


path(
    "careers/",
    views.careers,
    name="careers"
),

path(
    "careers/apply/<int:job_id>/",
    views.career_apply,
    name="career_apply"
),

path(
    "careers/submit-profile/",
    views.submit_candidate,
    name="submit_candidate"
),

path(
    "careers/verify-email/",
    views.verify_career_email,
    name="verify_career_email"
),

path(
    "careers/resend-otp/",
    views.resend_career_otp,
    name="resend_career_otp"
),

path(
    "dashboard/jobs/",
    views.manage_jobs,
    name="manage_jobs"
),

path(
    "dashboard/career-applicants/",
    views.manage_career_applicants,
    name="manage_career_applicants"
),


]