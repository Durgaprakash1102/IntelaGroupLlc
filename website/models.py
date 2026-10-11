from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):

    SUPERUSER = "SUPERUSER"
    ADMIN_HR = "ADMIN_HR"

    ROLE_CHOICES = (
        (SUPERUSER, "Superuser"),
        (ADMIN_HR, "Admin / HR"),
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ADMIN_HR
    )

    email_verified = models.BooleanField(
        default=False
    )

    otp = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    otp_created_at = models.DateTimeField(
        blank=True,
        null=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    def __str__(self):
        return self.email

    @property
    def is_superuser_role(self):
        return self.role == self.SUPERUSER

    @property
    def is_admin_hr(self):
        return self.role == self.ADMIN_HR


class Service(models.Model):

    title = models.CharField(
        max_length=200
    )

    short_description = models.CharField(
        max_length=300
    )

    description = models.TextField()

    

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=50, blank=True)
    alternate_phone = models.CharField(max_length=50, blank=True)
    whatsapp_number = models.CharField(max_length=50, blank=True)

    email = models.EmailField(blank=True)

    website = models.URLField(blank=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Details"
        verbose_name_plural = "Company Details"

    def __str__(self):
        return self.company_name


class CompanyLocation(models.Model):
    company = models.ForeignKey(
        CompanyDetails,
        on_delete=models.CASCADE,
        related_name="locations"
    )

    name = models.CharField(max_length=200)

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    map_link = models.URLField(
        blank=True,
        help_text="Google Maps URL"
    )

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        parts = [
            self.address,
            self.city,
            self.state,
            self.country,
        ]

        return ", ".join(
            part.strip()
            for part in parts
            if part and part.strip()
        )

class ContactMessage(models.Model):

    NEW = "NEW"
    READ = "READ"
    REPLIED = "REPLIED"

    STATUS_CHOICES = (
        (NEW, "New"),
        (READ, "Read"),
        (REPLIED, "Replied"),
    )

    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NEW
    )

    admin_reply = models.TextField(
        blank=True
    )

    replied_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_replies"
    )

    replied_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class JobPosting(models.Model):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"
    REMOTE = "REMOTE"

    EMPLOYMENT_TYPE_CHOICES = (
        (FULL_TIME, "Full Time"),
        (PART_TIME, "Part Time"),
        (CONTRACT, "Contract"),
        (INTERNSHIP, "Internship"),
        (REMOTE, "Remote"),
    )

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=200, blank=True)

    employment_type = models.CharField(
        max_length=30,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=FULL_TIME
    )

    experience = models.CharField(
        max_length=150,
        blank=True
    )

    salary = models.CharField(
        max_length=150,
        blank=True
    )

    short_description = models.CharField(max_length=300)

    description = models.TextField()

    requirements = models.TextField(
        blank=True
    )

    responsibilities = models.TextField(
        blank=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    posted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_postings"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class CareerApplicant(models.Model):
    APPLIED = "APPLIED"
    SCREENING = "SCREENING"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW = "INTERVIEW"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

    STATUS_CHOICES = (
        (APPLIED, "Applied"),
        (SCREENING, "Screening"),
        (SHORTLISTED, "Shortlisted"),
        (INTERVIEW, "Interview"),
        (SELECTED, "Selected"),
        (REJECTED, "Rejected"),
    )

    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    current_location = models.CharField(
        max_length=200,
        blank=True
    )

    experience = models.CharField(
        max_length=150,
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    resume = models.FileField(
        upload_to="career_resumes/"
    )

    cover_letter = models.TextField(
        blank=True
    )

    email_verified = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=APPLIED
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.name} - {self.job.title}"


class CandidateSubmission(models.Model):
    NEW = "NEW"
    REVIEWING = "REVIEWING"
    SHORTLISTED = "SHORTLISTED"
    CONTACTED = "CONTACTED"
    REJECTED = "REJECTED"

    STATUS_CHOICES = (
        (NEW, "New"),
        (REVIEWING, "Reviewing"),
        (SHORTLISTED, "Shortlisted"),
        (CONTACTED, "Contacted"),
        (REJECTED, "Rejected"),
    )

    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    current_location = models.CharField(
        max_length=200,
        blank=True
    )

    experience = models.CharField(
        max_length=150,
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    resume = models.FileField(
        upload_to="candidate_submissions/"
    )

    cover_letter = models.TextField(
        blank=True
    )

    email_verified = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=NEW
    )

    admin_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - General Candidate"


class CareerApplicationOTP(models.Model):
    JOB_APPLICATION = "JOB_APPLICATION"
    GENERAL_CANDIDATE = "GENERAL_CANDIDATE"

    TYPE_CHOICES = (
        (JOB_APPLICATION, "Job Application"),
        (GENERAL_CANDIDATE, "General Candidate"),
    )

    email = models.EmailField()

    verification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="career_otps"
    )

    otp = models.CharField(max_length=6)

    otp_created_at = models.DateTimeField(
        auto_now=True
    )

    verified = models.BooleanField(
        default=False
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.email} - {self.verification_type}"


from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.designation}"


from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=200)

    logo = models.ImageField(
        upload_to="partners/",
        blank=True,
        null=True,
    )

    website_url = models.URLField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name


class ClientTestimonial(models.Model):
    client_name = models.CharField(max_length=200)

    designation = models.CharField(
        max_length=200,
        blank=True,
    )

    company_name = models.CharField(
        max_length=200,
        blank=True,
    )

    testimonial = models.TextField()

    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
        help_text="Rating from 1 to 5",
    )

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Client Testimonial"
        verbose_name_plural = "Client Testimonials"

    def __str__(self):
        return f"{self.client_name} - {self.company_name or 'Client'}"
