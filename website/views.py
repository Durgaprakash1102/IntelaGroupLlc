import os
import random

from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import *
from .models import *
from .utils import *
from django.contrib.auth import login, logout, update_session_auth_hash

# ============================================================
# HOME
# ============================================================

def home(request):
    context = {
        "home_clients": Partner.objects.filter(is_active=True).order_by(
            "display_order", "name"
        ),
        "testimonials": ClientTestimonial.objects.filter(
            is_active=True
        ).order_by("display_order", "-created_at"),
    }

    return render(request, "website/home.html", context)

# ============================================================
# ABOUT
# ============================================================

from .models import TeamMember


def about(request):
    team_members = TeamMember.objects.filter(
        is_active=True
    ).order_by("display_order", "name")

    return render(
        request,
        "website/about.html",
        {
            "team_members": team_members,
        }
    )

def industries(request):
    return render(request, "website/industries.html")

# ============================================================
# SUPERUSER SIGNUP
# ============================================================

def superuser_signup(request):

    # Only one superuser role account can be created
    

    if request.method == "POST":

        form = SuperuserSignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = User.SUPERUSER

            user.is_staff = True
            user.is_superuser = True
            user.is_active = True

            # Superuser email is automatically verified
            user.email_verified = True

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            messages.success(
                request,
                "Superuser account created successfully. You can now login."
            )

            return redirect("website:login")

    else:
        form = SuperuserSignupForm()

    return render(
        request,
        "website/superuser_signup.html",
        {
            "form": form
        }
    )


# ============================================================
# ADMIN / HR SIGNUP
# ============================================================

def admin_signup(request):

    if request.method == "POST":

        form = AdminHRSignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = User.ADMIN_HR

            user.is_staff = True
            user.is_superuser = False
            user.is_active = False

            user.email_verified = False

            user.set_password(
                form.cleaned_data["password"]
            )

            otp = generate_otp()

            user.otp = otp
            user.otp_created_at = timezone.now()

            user.save()

            send_mail(
                subject="Intela Group - Email Verification OTP",
                message=(
                    f"Your Intela Group verification OTP is: {otp}\n\n"
                    "This OTP is valid for a limited time."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session["registration_user_id"] = user.id

            return redirect(
                "website:verify_registration_otp"
            )

    else:
        form = AdminHRSignupForm()

    return render(
        request,
        "website/admin_signup.html",
        {
            "form": form
        }
    )


# ============================================================
# REGISTRATION OTP
# ============================================================

def verify_registration_otp(request):

    user_id = request.session.get(
        "registration_user_id"
    )

    if not user_id:
        messages.error(
            request,
            "Registration session expired."
        )
        return redirect("website:admin_signup")

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == "POST":

        form = OTPForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data["otp"]

            if user.otp != entered_otp:

                form.add_error(
                    "otp",
                    "Invalid OTP."
                )

            else:

                # OTP expiration - 10 minutes
                if (
                    user.otp_created_at
                    and
                    timezone.now() >
                    user.otp_created_at +
                    timezone.timedelta(minutes=10)
                ):

                    form.add_error(
                        "otp",
                        "OTP has expired. Please register again."
                    )

                else:

                    user.email_verified = True
                    user.is_active = True
                    user.otp = None
                    user.otp_created_at = None

                    user.save()

                    request.session.pop(
                        "registration_user_id",
                        None
                    )

                    messages.success(
                        request,
                        "Email verified successfully. You can now login."
                    )

                    return redirect(
                        "website:login"
                    )

    else:
        form = OTPForm()

    return render(
        request,
        "website/verify_otp.html",
        {
            "form": form,
            "title": "Verify Email"
        }
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("website:dashboard")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            user = form.cleaned_data["user"]

            # Generate login OTP
            otp = generate_otp()

            user.otp = otp
            user.otp_created_at = timezone.now()

            user.save(
                update_fields=[
                    "otp",
                    "otp_created_at"
                ]
            )

            send_mail(
                subject="Intela Group - Login OTP",
                message=(
                    f"Your Intela Group login OTP is: {otp}\n\n"
                    "This OTP is valid for 10 minutes."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session["login_user_id"] = user.id

            return redirect(
                "website:verify_login_otp"
            )

    else:
        form = LoginForm()

    return render(
        request,
        "website/login.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGIN OTP
# ============================================================

def verify_login_otp(request):

    user_id = request.session.get(
        "login_user_id"
    )

    if not user_id:
        messages.error(
            request,
            "Login session expired."
        )
        return redirect("website:login")

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == "POST":

        form = OTPForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data["otp"]

            if user.otp != entered_otp:

                form.add_error(
                    "otp",
                    "Invalid OTP."
                )

            elif (
                user.otp_created_at
                and
                timezone.now() >
                user.otp_created_at +
                timezone.timedelta(minutes=10)
            ):

                form.add_error(
                    "otp",
                    "OTP has expired."
                )

            else:

                user.otp = None
                user.otp_created_at = None
                user.save(
                    update_fields=[
                        "otp",
                        "otp_created_at"
                    ]
                )

                login(
                    request,
                    user,
                    backend="website.backends.MultiFieldAuthenticationBackend"
                )

                request.session.pop(
                    "login_user_id",
                    None
                )

                return redirect(
                    "website:dashboard"
                )

    else:
        form = OTPForm()

    return render(
        request,
        "website/verify_otp.html",
        {
            "form": form,
            "title": "Verify Login OTP"
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("website:login")


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    return render(
        request,
        "website/dashboard.html"
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

def forgot_password(request):

    if request.method == "POST":

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            identifier = form.cleaned_data["identifier"]

            user = None

            # ------------------------------------------------
            # Search by username
            # ------------------------------------------------

            try:
                user = User.objects.get(
                    username__iexact=identifier
                )

            except User.DoesNotExist:
                pass

            # ------------------------------------------------
            # Search by email
            # ------------------------------------------------

            if user is None:

                try:
                    user = User.objects.get(
                        email__iexact=identifier
                    )

                except User.DoesNotExist:
                    pass

            # ------------------------------------------------
            # Search by phone
            # ------------------------------------------------

            if user is None:

                try:
                    user = User.objects.get(
                        phone_number=identifier
                    )

                except User.DoesNotExist:
                    pass

            # ------------------------------------------------
            # User not found
            # ------------------------------------------------

            if user is None:

                form.add_error(
                    "identifier",
                    "No account was found with those details."
                )

            elif not user.is_active:

                form.add_error(
                    "identifier",
                    "This account is inactive. Please contact the administrator."
                )

            else:

                # Generate password-reset OTP
                otp = generate_otp()

                user.otp = otp
                user.otp_created_at = timezone.now()

                user.save(
                    update_fields=[
                        "otp",
                        "otp_created_at"
                    ]
                )

                send_mail(
                    subject="Intela Group - Password Reset OTP",
                    message=(
                        f"Your Intela Group password reset OTP is: {otp}\n\n"
                        "This OTP is valid for 10 minutes.\n\n"
                        "If you did not request a password reset, please ignore this email."
                    ),
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                request.session["password_reset_user_id"] = user.id

                return redirect(
                    "website:verify_password_otp"
                )

    else:
        form = ForgotPasswordForm()

    return render(
        request,
        "website/forgot_password.html",
        {
            "form": form
        }
    )


# ============================================================
# FORGOT PASSWORD OTP
# ============================================================

def verify_password_otp(request):

    user_id = request.session.get(
        "password_reset_user_id"
    )

    if not user_id:

        messages.error(
            request,
            "Password reset session expired."
        )

        return redirect(
            "website:forgot_password"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == "POST":

        form = OTPForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data["otp"]

            if user.otp != entered_otp:

                form.add_error(
                    "otp",
                    "Invalid OTP."
                )

            elif (
                user.otp_created_at
                and
                timezone.now() >
                user.otp_created_at +
                timezone.timedelta(minutes=10)
            ):

                form.add_error(
                    "otp",
                    "OTP has expired. Please request a new OTP."
                )

            else:

                # OTP is valid.
                # Do NOT change the password yet.
                # Only mark password reset as verified.

                request.session[
                    "password_reset_verified"
                ] = True

                return redirect(
                    "website:reset_password"
                )

    else:
        form = OTPForm()

    return render(
        request,
        "website/verify_otp.html",
        {
            "form": form,
            "title": "Verify Password Reset OTP"
        }
    )


# ============================================================
# RESET PASSWORD
# ============================================================

def reset_password(request):

    user_id = request.session.get(
        "password_reset_user_id"
    )

    verified = request.session.get(
        "password_reset_verified"
    )

    if not user_id or not verified:

        messages.error(
            request,
            "Please verify your OTP first."
        )

        return redirect(
            "website:forgot_password"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == "POST":

        form = NewPasswordForm(request.POST)

        if form.is_valid():

            new_password = form.cleaned_data[
                "new_password"
            ]

            # IMPORTANT:
            # set_password() hashes the password correctly.
            user.set_password(new_password)

            # Remove reset OTP
            user.otp = None
            user.otp_created_at = None

            user.save()

            # Clear reset session
            request.session.pop(
                "password_reset_user_id",
                None
            )

            request.session.pop(
                "password_reset_verified",
                None
            )

            messages.success(
                request,
                "Password reset successfully. You can now login."
            )

            return redirect(
                "website:login"
            )

    else:
        form = NewPasswordForm()

    return render(
        request,
        "website/reset_password.html",
        {
            "form": form
        }
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

@login_required
def change_password(request):

    if request.method == "POST":

        form = ChangePasswordForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            new_password = form.cleaned_data[
                "new_password"
            ]

            # IMPORTANT:
            # Always use set_password().
            # Never assign password directly.
            request.user.set_password(
                new_password
            )

            request.user.save()

            # Keep the current user logged in.
            update_session_auth_hash(
                request,
                request.user
            )

            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect(
                "website:dashboard"
            )

    else:

        form = ChangePasswordForm(
            request.user
        )

    return render(
        request,
        "website/change_password.html",
        {
            "form": form
        }
    )

# ============================================================
# USER MANAGEMENT
# ============================================================

@login_required
def users_list(request):

    # Only Superuser can manage users
    if request.user.role != User.SUPERUSER:
        messages.error(
            request,
            "You do not have permission to manage users."
        )
        return redirect("website:dashboard")

    users = User.objects.all().order_by("-date_joined")

    return render(
        request,
        "website/users.html",
        {
            "users": users
        }
    )


@login_required
def create_admin_hr(request):

    # Only Superuser can create Admin/HR
    if request.user.role != User.SUPERUSER:
        messages.error(
            request,
            "You do not have permission to create users."
        )
        return redirect("website:dashboard")

    if request.method == "POST":

        form = AdminHRCreateForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = User.ADMIN_HR

            user.is_staff = True
            user.is_superuser = False
            user.is_active = True

            # Users created directly by Superuser
            # do not need email OTP verification.
            user.email_verified = True

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            messages.success(
                request,
                "Admin / HR user created successfully."
            )

            return redirect(
                "website:users_list"
            )

    else:
        form = AdminHRCreateForm()

    return render(
        request,
        "website/create_admin_hr.html",
        {
            "form": form
        }
    )


@login_required
def toggle_user_status(request, user_id):

    # Only Superuser can activate/deactivate users
    if request.user.role != User.SUPERUSER:
        messages.error(
            request,
            "You do not have permission to change user status."
        )
        return redirect("website:dashboard")

    user = get_object_or_404(
        User,
        id=user_id
    )

    # Never allow the superuser to deactivate themselves
    if user.id == request.user.id:

        messages.error(
            request,
            "You cannot deactivate your own account."
        )

        return redirect(
            "website:users_list"
        )

    # Only Admin/HR accounts can be managed here
    if user.role != User.ADMIN_HR:

        messages.error(
            request,
            "Only Admin / HR accounts can be managed here."
        )

        return redirect(
            "website:users_list"
        )

    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])

    if user.is_active:

        messages.success(
            request,
            f"{user.username} has been activated."
        )

    else:

        messages.success(
            request,
            f"{user.username} has been deactivated."
        )

    return redirect(
        "website:users_list"
    )

# ============================================================
# PUBLIC SERVICES
# ============================================================

def services(request):

    service_list = Service.objects.filter(
        is_active=True
    ).order_by("title")

    return render(
        request,
        "website/services.html",
        {
            "services": service_list
        }
    )

def service_detail(request, pk):
    service = get_object_or_404(
        Service,
        pk=pk,
        is_active=True
    )

    return render(
        request,
        "website/service_detail.html",
        {"service": service}
    )

# ============================================================
# SERVICE MANAGEMENT
# CREATE + EDIT ON SAME PAGE
# ============================================================

@login_required
def manage_services(request):

    if request.user.role not in [
        User.SUPERUSER,
        User.ADMIN_HR,
    ]:
        messages.error(
            request,
            "You do not have permission to manage services."
        )

        return redirect(
            "website:dashboard"
        )

    edit_id = request.GET.get("edit")

    editing_service = None

    if edit_id:

        editing_service = get_object_or_404(
            Service,
            id=edit_id
        )

    if request.method == "POST":

        service_id = request.POST.get(
            "service_id"
        )

        if service_id:

            service = get_object_or_404(
                Service,
                id=service_id
            )

            form = ServiceForm(
                request.POST,
                request.FILES,
                instance=service
            )

            action = "updated"

        else:

            form = ServiceForm(
                request.POST,
                request.FILES
            )

            action = "created"

        if form.is_valid():

            service = form.save()

            if action == "created":

                messages.success(
                    request,
                    f'"{service.title}" was created successfully.'
                )

            else:

                messages.success(
                    request,
                    f'"{service.title}" was updated successfully.'
                )

            return redirect(
                "website:manage_services"
            )

    else:

        if editing_service:

            form = ServiceForm(
                instance=editing_service
            )

        else:

            form = ServiceForm()

    service_list = Service.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "website/manage_services.html",
        {
            "form": form,
            "services": service_list,
            "editing_service": editing_service,
        }
    )


# ============================================================
# DELETE SERVICE
# NO SEPARATE DELETE PAGE
# ============================================================

@login_required
def delete_service(request, service_id):

    if request.user.role not in [
        User.SUPERUSER,
        User.ADMIN_HR,
    ]:
        messages.error(
            request,
            "You do not have permission to delete services."
        )

        return redirect(
            "website:dashboard"
        )

    if request.method != "POST":

        return redirect(
            "website:manage_services"
        )

    service = get_object_or_404(
        Service,
        id=service_id
    )

    service_title = service.title

    service.delete()

    messages.success(
        request,
        f'"{service_title}" was deleted successfully.'
    )

    return redirect(
        "website:manage_services"
    )


# ============================================================
# ACTIVATE / DEACTIVATE SERVICE
# ============================================================

@login_required
def toggle_service_status(
    request,
    service_id
):

    if request.user.role not in [
        User.SUPERUSER,
        User.ADMIN_HR,
    ]:
        messages.error(
            request,
            "You do not have permission to change service status."
        )

        return redirect(
            "website:dashboard"
        )

    if request.method != "POST":

        return redirect(
            "website:manage_services"
        )

    service = get_object_or_404(
        Service,
        id=service_id
    )

    service.is_active = not service.is_active

    service.save(
        update_fields=[
            "is_active",
            "updated_at",
        ]
    )

    if service.is_active:

        messages.success(
            request,
            f'"{service.title}" is now active.'
        )

    else:

        messages.success(
            request,
            f'"{service.title}" is now inactive.'
        )

    return redirect(
        "website:manage_services"
    )

@login_required
def manage_company_contact(request):

    if request.user.role not in [
        User.SUPERUSER,
        User.ADMIN_HR
    ]:

        messages.error(
            request,
            "You do not have permission to manage company contact details."
        )

        return redirect(
            "website:dashboard"
        )

    # ==========================================
    # COMPANY
    # ==========================================

    company = CompanyDetails.objects.first()

    if not company:

        company = CompanyDetails.objects.create(
            company_name="Intela Group"
        )

    # ==========================================
    # LOCATION EDIT
    # ==========================================

    edit_location_id = request.GET.get(
        "edit_location"
    )

    editing_location = None

    if edit_location_id:

        editing_location = get_object_or_404(
            CompanyLocation,
            id=edit_location_id,
            company=company
        )

    # ==========================================
    # SELECTED CONTACT MESSAGE
    # ==========================================

    message_id = request.GET.get(
        "message"
    )

    selected_message = None

    if message_id:

        selected_message = get_object_or_404(
            ContactMessage,
            id=message_id
        )

        # Automatically mark NEW message as READ
        # when opened by admin.

        if selected_message.status == ContactMessage.NEW:

            selected_message.status = ContactMessage.READ

            selected_message.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

    # ==========================================
    # POST ACTIONS
    # ==========================================

    if request.method == "POST":

        action = request.POST.get(
            "action"
        )

        # --------------------------------------
        # COMPANY DETAILS
        # --------------------------------------

        if action == "company_details":

            company_form = CompanyDetailsForm(
                request.POST,
                instance=company
            )

            if company_form.is_valid():

                company_form.save()

                messages.success(
                    request,
                    "Company details updated successfully."
                )

                return redirect(
                    "website:manage_company_contact"
                )

        # --------------------------------------
        # CREATE / UPDATE LOCATION
        # --------------------------------------

        elif action == "location":

            location_id = request.POST.get(
                "location_id"
            )

            if location_id:

                location = get_object_or_404(
                    CompanyLocation,
                    id=location_id,
                    company=company
                )

                location_form = CompanyLocationForm(
                    request.POST,
                    instance=location
                )

                success_message = (
                    "Company location updated successfully."
                )

            else:

                location_form = CompanyLocationForm(
                    request.POST
                )

                success_message = (
                    "Company location added successfully."
                )

            if location_form.is_valid():

                location = location_form.save(
                    commit=False
                )

                location.company = company

                location.save()

                messages.success(
                    request,
                    success_message
                )

                return redirect(
                    "website:manage_company_contact"
                )

        # --------------------------------------
        # TOGGLE LOCATION
        # --------------------------------------

        elif action == "toggle_location":

            location = get_object_or_404(
                CompanyLocation,
                id=request.POST.get("location_id"),
                company=company
            )

            location.is_active = (
                not location.is_active
            )

            location.save(
                update_fields=[
                    "is_active",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                "Location status updated successfully."
            )

            return redirect(
                "website:manage_company_contact"
            )

        # --------------------------------------
        # DELETE LOCATION
        # --------------------------------------

        elif action == "delete_location":

            location = get_object_or_404(
                CompanyLocation,
                id=request.POST.get("location_id"),
                company=company
            )

            location_name = location.name

            location.delete()

            messages.success(
                request,
                f'"{location_name}" deleted successfully.'
            )

            return redirect(
                "website:manage_company_contact"
            )

        # --------------------------------------
        # MARK MESSAGE READ
        # --------------------------------------

        elif action == "mark_message_read":

            contact_message = get_object_or_404(
                ContactMessage,
                id=request.POST.get("message_id")
            )

            contact_message.status = (
                ContactMessage.READ
            )

            contact_message.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            messages.success(
                request,
                "Message marked as read."
            )

            return redirect(
                "website:manage_company_contact"
            )

        # --------------------------------------
        # REPLY TO CONTACT MESSAGE
        # --------------------------------------

        elif action == "reply_message":

            contact_message = get_object_or_404(
                ContactMessage,
                id=request.POST.get("message_id")
            )

            reply_form = ContactReplyForm(
                request.POST,
                instance=contact_message
            )

            if reply_form.is_valid():

                reply_text = reply_form.cleaned_data[
                    "admin_reply"
                ]

                try:

                    send_mail(
                        subject=(
                            f"Re: {contact_message.subject}"
                        ),

                        message=(
                            f"Dear {contact_message.name},\n\n"
                            f"{reply_text}\n\n"
                            "Regards,\n"
                            f"{company.company_name}"
                        ),

                        from_email=settings.DEFAULT_FROM_EMAIL,

                        recipient_list=[
                            contact_message.email
                        ],

                        fail_silently=False,
                    )

                except Exception:

                    messages.error(
                        request,
                        "The reply email could not be sent. "
                        "Please check the email configuration."
                    )

                    return redirect(
                        f"{reverse('website:manage_company_contact')}"
                        f"?message={contact_message.id}#contact-messages"
                    )

                # Save as replied only AFTER
                # email has been sent successfully.

                contact_message.admin_reply = (
                    reply_text
                )

                contact_message.status = (
                    ContactMessage.REPLIED
                )

                contact_message.replied_by = (
                    request.user
                )

                contact_message.replied_at = (
                    timezone.now()
                )

                contact_message.save()

                messages.success(
                    request,
                    f"Reply sent successfully to "
                    f"{contact_message.email}."
                )

                return redirect(
                    f"{reverse('website:manage_company_contact')}"
                    f"?message={contact_message.id}#contact-messages"
                )

        # --------------------------------------
        # DELETE CONTACT MESSAGE
        # --------------------------------------

        elif action == "delete_message":

            contact_message = get_object_or_404(
                ContactMessage,
                id=request.POST.get("message_id")
            )

            contact_message.delete()

            messages.success(
                request,
                "Contact message deleted successfully."
            )

            return redirect(
                "website:manage_company_contact"
            )

    # ==========================================
    # DEFAULT FORMS
    # ==========================================

    company_form = CompanyDetailsForm(
        instance=company
    )

    if editing_location:

        location_form = CompanyLocationForm(
            instance=editing_location
        )

    else:

        location_form = CompanyLocationForm()

    if selected_message:

        reply_form = ContactReplyForm(
            instance=selected_message
        )

    else:

        reply_form = ContactReplyForm()

    # ==========================================
    # DATA
    # ==========================================

    locations = CompanyLocation.objects.filter(
        company=company
    ).order_by(
        "display_order",
        "name"
    )

    contact_messages = ContactMessage.objects.all()

    new_message_count = ContactMessage.objects.filter(
        status=ContactMessage.NEW
    ).count()

    return render(
        request,
        "website/manage_company_contact.html",
        {
            "company": company,

            "company_form": company_form,

            "location_form": location_form,

            "locations": locations,

            "editing_location": editing_location,

            "contact_messages": contact_messages,

            "selected_message": selected_message,

            "reply_form": reply_form,

            "new_message_count": new_message_count,
        }
    )

def contact(request):

    company = CompanyDetails.objects.first()

    locations = CompanyLocation.objects.none()

    if company:
        locations = CompanyLocation.objects.filter(
            company=company,
            is_active=True
        ).order_by(
            "display_order",
            "name"
        )

    if request.method == "POST":

        form = PublicContactForm(
            request.POST
        )

        if form.is_valid():

            contact_message = form.save()

            # --------------------------------
            # NOTIFY COMPANY / ADMIN
            # --------------------------------

            if company and company.email:

                try:

                    send_mail(
                        subject=(
                            "New Website Enquiry - "
                            f"{contact_message.subject}"
                        ),

                        message=(
                            "A new contact enquiry has been "
                            "submitted through the website.\n\n"

                            f"Name: {contact_message.name}\n"
                            f"Email: {contact_message.email}\n"
                            f"Phone: "
                            f"{contact_message.phone or 'Not provided'}\n\n"

                            f"Subject: {contact_message.subject}\n\n"

                            "Message:\n"
                            f"{contact_message.message}\n\n"

                            "Please login to the Intela Group "
                            "dashboard to reply."
                        ),

                        from_email=settings.DEFAULT_FROM_EMAIL,

                        recipient_list=[
                            company.email
                        ],

                        fail_silently=False,
                    )

                except Exception:
                    # The enquiry has already been saved.
                    # Don't make the visitor resubmit because
                    # the notification email failed.
                    pass

            messages.success(
                request,
                "Thank you for contacting us. "
                "Your message has been submitted successfully."
            )

            return redirect(
                "website:contact"
            )

    else:

        form = PublicContactForm()

    return render(
        request,
        "website/contact.html",
        {
            "company": company,
            "locations": locations,
            "form": form,
        }
    )


def generate_career_otp():
    return str(random.randint(100000, 999999))


def careers(request):
    jobs = JobPosting.objects.filter(
        is_active=True
    ).order_by("-created_at")

    job_form = CareerApplicantForm()
    candidate_form = CandidateSubmissionForm()

    otp_required = request.session.get("career_otp_required", False)
    otp_type = request.session.get("career_otp_type")

    otp_email = request.session.get("career_otp_email")

    return render(
        request,
        "website/careers.html",
        {
            "jobs": jobs,
            "job_form": job_form,
            "candidate_form": candidate_form,
            "otp_required": otp_required,
            "otp_type": otp_type,
            "otp_email": otp_email,
        }
    )


def career_apply(request, job_id):
    job = get_object_or_404(
        JobPosting,
        id=job_id,
        is_active=True
    )

    if request.method != "POST":
        return redirect("website:careers")

    form = CareerApplicantForm(
        request.POST,
        request.FILES
    )

    if not form.is_valid():
        jobs = JobPosting.objects.filter(
            is_active=True
        ).order_by("-created_at")

        return render(
            request,
            "website/careers.html",
            {
                "jobs": jobs,
                "job_form": form,
                "candidate_form": CandidateSubmissionForm(),
                "selected_job": job,
            }
        )

    email = form.cleaned_data["email"].strip().lower()

    # Remove previous pending OTPs for this email/job.
    CareerApplicationOTP.objects.filter(
        email=email,
        verification_type=CareerApplicationOTP.JOB_APPLICATION,
        job=job
    ).delete()

    otp = generate_career_otp()

    CareerApplicationOTP.objects.create(
        email=email,
        verification_type=CareerApplicationOTP.JOB_APPLICATION,
        job=job,
        otp=otp,
    )

    # Save normal form data in session.
    request.session["career_otp_required"] = True
    request.session["career_otp_type"] = "JOB_APPLICATION"
    request.session["career_otp_email"] = email
    request.session["career_otp_id"] = CareerApplicationOTP.objects.latest(
        "id"
    ).id

    request.session["career_job_id"] = job.id

    request.session["career_candidate_data"] = {
        "name": form.cleaned_data["name"],
        "email": email,
        "phone": form.cleaned_data["phone"],
        "current_location": form.cleaned_data["current_location"],
        "experience": form.cleaned_data["experience"],
        "skills": form.cleaned_data["skills"],
        "cover_letter": form.cleaned_data["cover_letter"],
    }

    uploaded_resume = request.FILES.get("resume")

    if uploaded_resume:
        pending_dir = os.path.join(
            settings.MEDIA_ROOT,
            "pending_career"
        )

        os.makedirs(
            pending_dir,
            exist_ok=True
        )

        safe_name = (
            f"job_{job.id}_"
            f"{timezone.now().strftime('%Y%m%d%H%M%S')}_"
            f"{uploaded_resume.name}"
        )

        pending_path = os.path.join(
            pending_dir,
            safe_name
        )

        with open(pending_path, "wb+") as destination:
            for chunk in uploaded_resume.chunks():
                destination.write(chunk)

        request.session["career_pending_resume"] = pending_path

    send_mail(
        subject="Verify Your Email - Intela Group Careers",
        message=(
            f"Hello {form.cleaned_data['name']},\n\n"
            f"Thank you for applying for the "
            f"{job.title} position at Intela Group.\n\n"
            f"Your email verification OTP is:\n\n"
            f"{otp}\n\n"
            f"This OTP is valid for 10 minutes.\n\n"
            f"If you did not submit this application, "
            f"you can ignore this email.\n\n"
            f"Regards,\n"
            f"Intela Group"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(
        request,
        "A verification OTP has been sent to your email."
    )

    return redirect("website:careers")


def submit_candidate(request):
    if request.method != "POST":
        return redirect("website:careers")

    form = CandidateSubmissionForm(
        request.POST,
        request.FILES
    )

    if not form.is_valid():
        jobs = JobPosting.objects.filter(
            is_active=True
        ).order_by("-created_at")

        return render(
            request,
            "website/careers.html",
            {
                "jobs": jobs,
                "job_form": CareerApplicantForm(),
                "candidate_form": form,
            }
        )

    email = form.cleaned_data["email"].strip().lower()

    CareerApplicationOTP.objects.filter(
        email=email,
        verification_type=CareerApplicationOTP.GENERAL_CANDIDATE,
        job__isnull=True
    ).delete()

    otp = generate_career_otp()

    otp_record = CareerApplicationOTP.objects.create(
        email=email,
        verification_type=CareerApplicationOTP.GENERAL_CANDIDATE,
        otp=otp,
        job=None,
    )

    request.session["career_otp_required"] = True
    request.session["career_otp_type"] = "GENERAL_CANDIDATE"
    request.session["career_otp_email"] = email
    request.session["career_otp_id"] = otp_record.id

    request.session["career_candidate_data"] = {
        "name": form.cleaned_data["name"],
        "email": email,
        "phone": form.cleaned_data["phone"],
        "current_location": form.cleaned_data["current_location"],
        "experience": form.cleaned_data["experience"],
        "skills": form.cleaned_data["skills"],
        "cover_letter": form.cleaned_data["cover_letter"],
    }

    uploaded_resume = request.FILES.get("resume")

    if uploaded_resume:
        pending_dir = os.path.join(
            settings.MEDIA_ROOT,
            "pending_career"
        )

        os.makedirs(
            pending_dir,
            exist_ok=True
        )

        safe_name = (
            f"candidate_"
            f"{timezone.now().strftime('%Y%m%d%H%M%S')}_"
            f"{uploaded_resume.name}"
        )

        pending_path = os.path.join(
            pending_dir,
            safe_name
        )

        with open(pending_path, "wb+") as destination:
            for chunk in uploaded_resume.chunks():
                destination.write(chunk)

        request.session["career_pending_resume"] = pending_path

    send_mail(
        subject="Verify Your Email - Intela Group Careers",
        message=(
            f"Hello {form.cleaned_data['name']},\n\n"
            f"Thank you for your interest in Intela Group.\n\n"
            f"Your email verification OTP is:\n\n"
            f"{otp}\n\n"
            f"This OTP is valid for 10 minutes.\n\n"
            f"Regards,\n"
            f"Intela Group"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(
        request,
        "A verification OTP has been sent to your email."
    )

    return redirect("website:careers")


def verify_career_email(request):
    if request.method != "POST":
        return redirect("website:careers")

    otp_form = CareerOTPForm(request.POST)

    if not otp_form.is_valid():
        messages.error(
            request,
            "Please enter a valid 6-digit OTP."
        )
        return redirect("website:careers")

    otp_value = otp_form.cleaned_data["otp"]

    otp_id = request.session.get("career_otp_id")
    otp_type = request.session.get("career_otp_type")

    if not otp_id or not otp_type:
        messages.error(
            request,
            "Your verification session has expired. Please submit the form again."
        )
        return redirect("website:careers")

    try:
        otp_record = CareerApplicationOTP.objects.get(
            id=otp_id
        )
    except CareerApplicationOTP.DoesNotExist:
        messages.error(
            request,
            "Invalid verification session."
        )
        return redirect("website:careers")

    if otp_record.verified:
        messages.error(
            request,
            "This verification code has already been used."
        )
        return redirect("website:careers")

    if timezone.now() - otp_record.otp_created_at > timedelta(
        minutes=10
    ):
        otp_record.delete()

        messages.error(
            request,
            "The OTP has expired. Please request a new verification code."
        )

        return redirect("website:careers")

    if otp_record.attempts >= 5:
        messages.error(
            request,
            "Too many incorrect attempts. Please request a new OTP."
        )

        return redirect("website:careers")

    if otp_record.otp != otp_value:
        otp_record.attempts += 1
        otp_record.save(
            update_fields=["attempts"]
        )

        messages.error(
            request,
            "Invalid OTP. Please try again."
        )

        return redirect("website:careers")

    otp_record.verified = True
    otp_record.save(
        update_fields=["verified"]
    )

    candidate_data = request.session.get(
        "career_candidate_data"
    )

    pending_resume = request.session.get(
        "career_pending_resume"
    )

    if not candidate_data:
        messages.error(
            request,
            "Your application session has expired. Please submit the form again."
        )
        return redirect("website:careers")

    if otp_type == "JOB_APPLICATION":
        job_id = request.session.get(
            "career_job_id"
        )

        try:
            job = JobPosting.objects.get(
                id=job_id,
                is_active=True
            )
        except JobPosting.DoesNotExist:
            messages.error(
                request,
                "This job is no longer available."
            )
            return redirect("website:careers")

        application = CareerApplicant(
            job=job,
            name=candidate_data["name"],
            email=candidate_data["email"],
            phone=candidate_data["phone"],
            current_location=candidate_data["current_location"],
            experience=candidate_data["experience"],
            skills=candidate_data["skills"],
            cover_letter=candidate_data["cover_letter"],
            email_verified=True,
            status=CareerApplicant.APPLIED,
        )

        if pending_resume and os.path.exists(pending_resume):
            with open(pending_resume, "rb") as resume_file:
                application.resume.save(
                    os.path.basename(pending_resume),
                    File(resume_file),
                    save=False
                )

        application.save()

        # Notify the person who posted the job.
        if job.posted_by and job.posted_by.email:
            send_mail(
                subject=(
                    f"New Application Received - {job.title}"
                ),
                message=(
                    "A new application has been received "
                    "through the Intela Group website.\n\n"

                    f"Job: {job.title}\n"
                    f"Applicant: {application.name}\n"
                    f"Email: {application.email}\n"
                    f"Phone: {application.phone}\n"
                    f"Location: "
                    f"{application.current_location or 'Not provided'}\n"
                    f"Experience: "
                    f"{application.experience or 'Not provided'}\n\n"

                    "The applicant's resume and complete "
                    "application are available in the "
                    "Intela Group dashboard."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[job.posted_by.email],
                fail_silently=False,
            )

        success_message = (
            "Your email has been verified and your application "
            "has been submitted successfully."
        )

    else:
        company = CompanyDetails.objects.first()

        candidate = CandidateSubmission(
            name=candidate_data["name"],
            email=candidate_data["email"],
            phone=candidate_data["phone"],
            current_location=candidate_data["current_location"],
            experience=candidate_data["experience"],
            skills=candidate_data["skills"],
            cover_letter=candidate_data["cover_letter"],
            email_verified=True,
            status=CandidateSubmission.NEW,
        )

        if pending_resume and os.path.exists(pending_resume):
            with open(pending_resume, "rb") as resume_file:
                candidate.resume.save(
                    os.path.basename(pending_resume),
                    File(resume_file),
                    save=False
                )

        candidate.save()

        if company and company.email:
            send_mail(
                subject=(
                    "New Candidate Profile Submitted - "
                    "Intela Group"
                ),
                message=(
                    "A new candidate profile has been submitted "
                    "through the Intela Group careers page.\n\n"

                    f"Name: {candidate.name}\n"
                    f"Email: {candidate.email}\n"
                    f"Phone: {candidate.phone}\n"
                    f"Location: "
                    f"{candidate.current_location or 'Not provided'}\n"
                    f"Experience: "
                    f"{candidate.experience or 'Not provided'}\n\n"

                    "The candidate's resume and complete profile "
                    "are available in the Intela Group dashboard."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[company.email],
                fail_silently=False,
            )

        success_message = (
            "Your email has been verified and your profile "
            "has been submitted successfully."
        )

    # Remove temporary file.
    if pending_resume and os.path.exists(pending_resume):
        try:
            os.remove(pending_resume)
        except OSError:
            pass

    # Clear session.
    for key in [
        "career_otp_required",
        "career_otp_type",
        "career_otp_email",
        "career_otp_id",
        "career_job_id",
        "career_candidate_data",
        "career_pending_resume",
    ]:
        request.session.pop(key, None)

    messages.success(
        request,
        success_message
    )

    return redirect("website:careers")


def resend_career_otp(request):
    if request.method != "POST":
        return redirect("website:careers")

    otp_id = request.session.get("career_otp_id")

    if not otp_id:
        messages.error(
            request,
            "No active verification request was found."
        )
        return redirect("website:careers")

    try:
        old_otp = CareerApplicationOTP.objects.get(
            id=otp_id
        )
    except CareerApplicationOTP.DoesNotExist:
        messages.error(
            request,
            "Your verification session has expired."
        )
        return redirect("website:careers")

    if timezone.now() - old_otp.otp_created_at < timedelta(
        seconds=60
    ):
        messages.error(
            request,
            "Please wait at least 60 seconds before requesting another OTP."
        )
        return redirect("website:careers")

    new_otp = generate_career_otp()

    old_otp.otp = new_otp
    old_otp.otp_created_at = timezone.now()
    old_otp.attempts = 0
    old_otp.verified = False
    old_otp.save()

    request.session["career_otp_id"] = old_otp.id

    candidate_data = request.session.get(
        "career_candidate_data",
        {}
    )

    email = old_otp.email

    send_mail(
        subject="New Verification OTP - Intela Group",
        message=(
            f"Hello {candidate_data.get('name', 'Candidate')},\n\n"
            f"Your new Intela Group verification OTP is:\n\n"
            f"{new_otp}\n\n"
            f"This OTP is valid for 10 minutes.\n\n"
            f"Regards,\n"
            f"Intela Group"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(
        request,
        "A new OTP has been sent to your email."
    )

    return redirect("website:careers")

@login_required
def manage_jobs(request):
    if request.user.role not in [
        User.SUPERUSER,
        User.ADMIN_HR,
    ]:
        messages.error(
            request,
            "You do not have permission to manage jobs."
        )
        return redirect("website:dashboard")

    edit_id = request.GET.get("edit")
    editing_job = None

    if edit_id:
        editing_job = get_object_or_404(
            JobPosting,
            id=edit_id
        )

    if request.method == "POST":

        action = request.POST.get("action")

        # -----------------------------------------
        # CREATE / UPDATE JOB
        # -----------------------------------------
        if action in ["create_job", "update_job"]:

            job_id = request.POST.get("job_id")

            if job_id:
                job = get_object_or_404(
                    JobPosting,
                    id=job_id
                )

                form = JobPostingForm(
                    request.POST,
                    instance=job
                )

            else:
                form = JobPostingForm(
                    request.POST
                )

            if form.is_valid():

                job = form.save(
                    commit=False
                )

                # Only set the poster when creating.
                if not job.pk:
                    job.posted_by = request.user

                job.save()

                if job_id:
                    messages.success(
                        request,
                        f'"{job.title}" was updated successfully.'
                    )
                else:
                    messages.success(
                        request,
                        f'"{job.title}" was created successfully.'
                    )

                return redirect(
                    "website:manage_jobs"
                )

        # -----------------------------------------
        # DELETE JOB
        # -----------------------------------------
        elif action == "delete_job":

            job_id = request.POST.get(
                "job_id"
            )

            job = get_object_or_404(
                JobPosting,
                id=job_id
            )

            title = job.title

            job.delete()

            messages.success(
                request,
                f'"{title}" was deleted successfully.'
            )

            return redirect(
                "website:manage_jobs"
            )

        # -----------------------------------------
        # TOGGLE JOB STATUS
        # -----------------------------------------
        elif action == "toggle_job":

            job_id = request.POST.get(
                "job_id"
            )

            job = get_object_or_404(
                JobPosting,
                id=job_id
            )

            job.is_active = not job.is_active

            job.save(
                update_fields=[
                    "is_active",
                    "updated_at",
                ]
            )

            status = (
                "activated"
                if job.is_active
                else "deactivated"
            )

            messages.success(
                request,
                f'"{job.title}" was {status}.'
            )

            return redirect(
                "website:manage_jobs"
            )

    else:

        if editing_job:
            form = JobPostingForm(
                instance=editing_job
            )
        else:
            form = JobPostingForm()

    jobs = JobPosting.objects.select_related(
        "posted_by"
    ).all().order_by(
        "-created_at"
    )

    return render(
        request,
        "website/manage_jobs.html",
        {
            "form": form,
            "jobs": jobs,
            "editing_job": editing_job,
        }
    )

@login_required
def manage_career_applicants(request):
    if request.user.role not in [User.SUPERUSER, User.ADMIN_HR]:
        messages.error(
            request,
            "You do not have permission to manage career applicants."
        )
        return redirect("website:dashboard")

    # ---------------------------------------------------------
    # JOB FILTER
    # ---------------------------------------------------------
    selected_job_id = request.GET.get("job", "").strip()

    jobs = JobPosting.objects.all().order_by("-created_at")

    job_applications = CareerApplicant.objects.select_related(
        "job"
    ).all().order_by("-applied_at")

    selected_job = None

    if selected_job_id:
        try:
            selected_job = JobPosting.objects.get(id=selected_job_id)
            job_applications = job_applications.filter(
                job=selected_job
            )
        except (JobPosting.DoesNotExist, ValueError):
            selected_job_id = ""
            selected_job = None

    # ---------------------------------------------------------
    # POST ACTIONS
    # ---------------------------------------------------------
    if request.method == "POST":

        action = request.POST.get("action")

        # Keep currently selected job after POST
        current_job_id = request.POST.get(
            "selected_job_id",
            selected_job_id
        )

        # -----------------------------------------------------
        # DELETE JOB APPLICATION
        # -----------------------------------------------------
        if action == "delete_job_application":

            application_id = request.POST.get("application_id")

            application = get_object_or_404(
                CareerApplicant,
                id=application_id
            )

            applicant_name = application.name

            application.delete()

            messages.success(
                request,
                f"Application from {applicant_name} was deleted successfully."
            )

            if current_job_id:
                return redirect(
                    f"{reverse('website:manage_career_applicants')}?job={current_job_id}"
                )

            return redirect("website:manage_career_applicants")

        # -----------------------------------------------------
        # DELETE GENERAL CANDIDATE
        # -----------------------------------------------------
        elif action == "delete_candidate":

            candidate_id = request.POST.get("candidate_id")

            candidate = get_object_or_404(
                CandidateSubmission,
                id=candidate_id
            )

            candidate_name = candidate.name

            candidate.delete()

            messages.success(
                request,
                f"Candidate {candidate_name} was deleted successfully."
            )

            if current_job_id:
                return redirect(
                    f"{reverse('website:manage_career_applicants')}?job={current_job_id}"
                )

            return redirect("website:manage_career_applicants")

        # -----------------------------------------------------
        # UPDATE JOB APPLICATION STATUS
        # -----------------------------------------------------
        elif action == "update_job_application_status":

            application_id = request.POST.get("application_id")
            status = request.POST.get("status")

            application = get_object_or_404(
                CareerApplicant,
                id=application_id
            )

            valid_statuses = dict(
                CareerApplicant.STATUS_CHOICES
            )

            if status in valid_statuses:
                application.status = status
                application.save(update_fields=["status", "updated_at"])

                messages.success(
                    request,
                    f"Application status for {application.name} "
                    f"was updated to {valid_statuses[status]}."
                )
            else:
                messages.error(
                    request,
                    "Invalid application status."
                )

            if current_job_id:
                return redirect(
                    f"{reverse('website:manage_career_applicants')}?job={current_job_id}"
                )

            return redirect("website:manage_career_applicants")

        # -----------------------------------------------------
        # UPDATE GENERAL CANDIDATE STATUS
        # -----------------------------------------------------
        elif action == "update_candidate_status":

            candidate_id = request.POST.get("candidate_id")
            status = request.POST.get("status")

            candidate = get_object_or_404(
                CandidateSubmission,
                id=candidate_id
            )

            valid_statuses = dict(
                CandidateSubmission.STATUS_CHOICES
            )

            if status in valid_statuses:
                candidate.status = status
                candidate.save(update_fields=["status", "updated_at"])

                messages.success(
                    request,
                    f"Candidate status for {candidate.name} "
                    f"was updated to {valid_statuses[status]}."
                )
            else:
                messages.error(
                    request,
                    "Invalid candidate status."
                )

            if current_job_id:
                return redirect(
                    f"{reverse('website:manage_career_applicants')}?job={current_job_id}"
                )

            return redirect("website:manage_career_applicants")

    # ---------------------------------------------------------
    # COUNTS
    # ---------------------------------------------------------

    # Overall counts
    total_job_applications = CareerApplicant.objects.count()

    new_job_applications = CareerApplicant.objects.filter(
        status=CareerApplicant.APPLIED
    ).count()

    total_general_candidates = CandidateSubmission.objects.count()

    new_general_candidates = CandidateSubmission.objects.filter(
        status=CandidateSubmission.NEW
    ).count()

    # Filtered count for the selected job
    filtered_job_applications = job_applications.count()

    context = {
        "job_applications": job_applications,
        "general_candidates": CandidateSubmission.objects.all().order_by(
            "-created_at"
        ),

        "jobs": jobs,
        "selected_job": selected_job,
        "selected_job_id": selected_job_id,
        "filtered_job_applications": filtered_job_applications,

        "total_job_applications": total_job_applications,
        "new_job_applications": new_job_applications,
        "total_general_candidates": total_general_candidates,
        "new_general_candidates": new_general_candidates,

        "job_status_choices": CareerApplicant.STATUS_CHOICES,
        "candidate_status_choices": CandidateSubmission.STATUS_CHOICES,
    }

    return render(
        request,
        "website/career_applicants.html",
        context
    )

