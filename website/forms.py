from django import forms
from django.contrib.auth import authenticate
from .models import *


class SuperuserSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return None

        phone = phone.strip()

        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(
                "An account with this phone number already exists."
            )

        return phone

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class AdminHRSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return None

        phone = phone.strip()

        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(
                "An account with this phone number already exists."
            )

        return phone

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    identifier = forms.CharField(
        label="Username, Email or Phone Number",
        max_length=150
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")

        if not identifier or not password:
            return cleaned_data

        identifier = identifier.strip()

        user = authenticate(
            username=identifier,
            password=password
        )

        if user is None:
            raise forms.ValidationError(
                "Invalid username, email/phone number or password."
            )

        if not user.is_active:
            raise forms.ValidationError(
                "Your account has been deactivated. Please contact the administrator."
            )

        cleaned_data["user"] = user

        return cleaned_data


class OTPForm(forms.Form):
    otp = forms.CharField(
        label="OTP",
        max_length=6,
        min_length=6
    )

    def clean_otp(self):
        otp = self.cleaned_data["otp"].strip()

        if not otp.isdigit():
            raise forms.ValidationError("OTP must contain only numbers.")

        return otp


class ForgotPasswordForm(forms.Form):
    identifier = forms.CharField(
        label="Username, Email or Phone Number",
        max_length=150
    )

    def clean_identifier(self):
        identifier = self.cleaned_data["identifier"].strip()

        if not identifier:
            raise forms.ValidationError(
                "Please enter your username, email or phone number."
            )

        return identifier


class NewPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        min_length=8
    )

    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "New passwords do not match."
                )

        return cleaned_data


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        min_length=8
    )

    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        min_length=8
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")

        if not current_password:
            raise forms.ValidationError(
                "Please enter your current password."
            )

        # Directly check the stored password hash.
        # This avoids the PasswordChangeForm issue.
        if not self.user.check_password(current_password):
            raise forms.ValidationError(
                "Your current password is incorrect."
            )

        return current_password

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:

            if new_password != confirm_password:
                raise forms.ValidationError(
                    "New passwords do not match."
                )

            if len(new_password) < 8:
                raise forms.ValidationError(
                    "New password must contain at least 8 characters."
                )

        return cleaned_data

class AdminHRCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return None

        phone = phone.strip()

        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(
                "An account with this phone number already exists."
            )

        return phone

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

from django import forms

from .models import (
    User,
    Service,
)


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service

        fields = [
            "title",
            "short_description",
            "description",
            
            "image",
            "is_active",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter service title"
                }
            ),

            "short_description": forms.TextInput(
                attrs={
                    "placeholder": "Short description"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter complete service description",
                    "rows": 7
                }
            ),

            
            "image": forms.ClearableFileInput(),

            "is_active": forms.CheckboxInput(),
        }

    def clean_title(self):

        title = self.cleaned_data["title"].strip()

        if not title:
            raise forms.ValidationError(
                "Service title is required."
            )

        return title

    def clean_short_description(self):

        value = self.cleaned_data[
            "short_description"
        ].strip()

        if not value:
            raise forms.ValidationError(
                "Short description is required."
            )

        return value

    def clean_description(self):

        value = self.cleaned_data[
            "description"
        ].strip()

        if not value:
            raise forms.ValidationError(
                "Service description is required."
            )

        return value

class CompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails

        fields = [
            "company_name",
            "phone",
            "alternate_phone",
            "whatsapp_number",
            "email",
            "website",
            "facebook_url",
            "instagram_url",
            "linkedin_url",
            "youtube_url",
            "twitter_url",
        ]

        widgets = {
            "company_name": forms.TextInput(
                attrs={
                    "placeholder": "Intela Group"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number (with country code)"
                }
            ),

            "alternate_phone": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number (with country code)"
                }
            ),

            "whatsapp_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number (with country code)"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "info@intelagroup.com"
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com"
                }
            ),

            "facebook_url": forms.URLInput(
                attrs={
                    "placeholder": "Facebook URL"
                }
            ),

            "instagram_url": forms.URLInput(
                attrs={
                    "placeholder": "Instagram URL"
                }
            ),

            "linkedin_url": forms.URLInput(
                attrs={
                    "placeholder": "LinkedIn URL"
                }
            ),

            "youtube_url": forms.URLInput(
                attrs={
                    "placeholder": "YouTube URL"
                }
            ),

            "twitter_url": forms.URLInput(
                attrs={
                    "placeholder": "X / Twitter URL"
                }
            ),
        }


class CompanyLocationForm(forms.ModelForm):
    class Meta:
        model = CompanyLocation

        fields = [
            "name",
            "address",
            "city",
            "state",
            "country",
            "map_link",
            "is_active",
            "display_order",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Office Location"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "placeholder": "Complete office address",
                    "rows": 4
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "City Name"
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "State Name"
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "placeholder": "Country Name"
                }
            ),

            "map_link": forms.URLInput(
                attrs={
                    "placeholder": "https://maps.google.com/..."
                }
            ),

            "is_active": forms.CheckboxInput(),

            "display_order": forms.NumberInput(
                attrs={
                    "min": 0
                }
            ),
        }

class PublicContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your full name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your email address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your phone number",
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "How can we help you?",
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell us about your requirement...",
                    "rows": 6,
                }
            ),
        }


class ContactReplyForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "admin_reply",
        ]

        widgets = {
            "admin_reply": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your reply...",
                    "rows": 6,
                }
            ),
        }

    def clean_admin_reply(self):

        reply = self.cleaned_data.get(
            "admin_reply",
            ""
        ).strip()

        if not reply:
            raise forms.ValidationError(
                "Please enter a reply."
            )

        return reply


from django import forms
from .models import (
    JobPosting,
    CareerApplicant,
    CandidateSubmission,
)


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            "title",
            "department",
            "location",
            "employment_type",
            "experience",
            "salary",
            "short_description",
            "description",
            "requirements",
            "responsibilities",
            "deadline",
            "is_active",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Python Full Stack Developer",
            }),

            "department": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "IT / Development",
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your Location",
            }),

            "employment_type": forms.Select(attrs={
                "class": "form-control",
            }),

            "experience": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "2-4 years",
            }),

            "salary": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Your Salary",
            }),

            "short_description": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Short description of the position",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Describe the role...",
            }),

            "requirements": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Enter requirements, one per line...",
            }),

            "responsibilities": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Enter responsibilities, one per line...",
            }),

            "deadline": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }


class CareerApplicantForm(forms.ModelForm):
    class Meta:
        model = CareerApplicant

        fields = [
            "name",
            "email",
            "phone",
            "current_location",
            "experience",
            "skills",
            "resume",
            "cover_letter",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your full name",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Your email address",
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number (with country code)",
            }),

            "current_location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your Location",
            }),

            "experience": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: 3 years",
            }),

            "skills": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Python, Django, React, SQL...",
            }),

            "resume": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.doc,.docx",
            }),

            "cover_letter": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Tell us why you are a good fit...",
            }),
        }


class CandidateSubmissionForm(forms.ModelForm):
    class Meta:
        model = CandidateSubmission

        fields = [
            "name",
            "email",
            "phone",
            "current_location",
            "experience",
            "skills",
            "resume",
            "cover_letter",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your full name",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Your email address",
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number (with country code)",
            }),

            "current_location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your Location",
            }),

            "experience": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: 3 years",
            }),

            "skills": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Python, Django, React, SQL...",
            }),

            "resume": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.doc,.docx",
            }),

            "cover_letter": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Tell us about yourself...",
            }),
        }


class CareerOTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control otp-input",
            "placeholder": "Enter 6-digit OTP",
            "maxlength": "6",
            "autocomplete": "one-time-code",
        })
    )

