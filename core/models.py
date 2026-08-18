from django.db import models
from django.utils.text import slugify
import json


class Profile(models.Model):
    """Main profile information - single instance."""
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    professional_summary = models.TextField(help_text="Brief professional summary for hero section")
    about_me = models.TextField(help_text="Detailed about me narrative")
    hero_tagline = models.CharField(max_length=500, blank=True, help_text="Impactful hero statement")
    hero_subtitles = models.TextField(blank=True, help_text="Comma-separated typing animation texts")
    resume_file = models.FileField(upload_to='resume/', blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    certifications_count = models.PositiveIntegerField(default=0)
    meta_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    def get_hero_subtitles_list(self):
        if self.hero_subtitles:
            return [s.strip() for s in self.hero_subtitles.split(',')]
        return []


class Skill(models.Model):
    """Technical and soft skills."""
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Databases'),
        ('cloud', 'Cloud & DevOps'),
        ('enterprise', 'Enterprise Platforms'),
        ('state', 'State Management'),
        ('soft', 'Soft Skills'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.PositiveIntegerField(default=75, help_text="Proficiency level 0-100")
    icon_class = models.CharField(max_length=100, blank=True, help_text="Icon class or SVG identifier")
    color = models.CharField(max_length=7, blank=True, help_text="Hex color for skill card")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    """Work experience entries."""
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Overview description of the role")
    responsibilities = models.JSONField(default=list, blank=True, help_text="List of key responsibilities")
    achievements = models.JSONField(default=list, blank=True, help_text="List of achievements")
    technologies = models.JSONField(default=list, blank=True, help_text="Technologies used")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Experience"
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.title} at {self.company}"

    def duration_display(self):
        if self.is_current:
            return f"{self.start_date.strftime('%b %Y')} — Present"
        elif self.end_date:
            return f"{self.start_date.strftime('%b %Y')} — {self.end_date.strftime('%b %Y')}"
        return self.start_date.strftime('%b %Y')


class Project(models.Model):
    """Portfolio projects."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    tagline = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=200, blank=True)
    overview = models.TextField(help_text="Detailed project overview")
    problem_statement = models.TextField(blank=True)
    features = models.JSONField(default=list, blank=True, help_text="List of key features")
    challenges = models.JSONField(default=list, blank=True, help_text="Challenges faced and solutions")
    technologies = models.JSONField(default=list, blank=True, help_text="Technologies used")
    architecture = models.TextField(blank=True, help_text="Architecture description")
    lessons_learned = models.TextField(blank=True)
    github_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True)
    hero_image = models.ImageField(upload_to='projects/heroes/', blank=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    accent_color = models.CharField(max_length=7, default='#6C63FF', help_text="Accent color hex")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectScreenshot(models.Model):
    """Screenshots for projects."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='projects/screenshots/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Project Screenshot"

    def __str__(self):
        return f"{self.project.title} — Screenshot {self.order}"


class Certification(models.Model):
    """Professional certifications."""
    CATEGORY_CHOICES = [
        ('servicenow', 'ServiceNow'),
        ('cloud', 'Cloud'),
        ('programming', 'Programming'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    date_earned = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    verification_url = models.URLField(blank=True)
    badge_image = models.ImageField(upload_to='certifications/', blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date_earned']
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return self.name


class Education(models.Model):
    """Education history."""
    degree = models.CharField(max_length=300)
    field = models.CharField(max_length=200, blank=True)
    institution = models.CharField(max_length=300)
    graduation_year = models.PositiveIntegerField()
    gpa = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-graduation_year']
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class SocialLink(models.Model):
    """Social media and professional links."""
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('twitter', 'Twitter/X'),
        ('email', 'Email'),
        ('website', 'Website'),
        ('stackoverflow', 'Stack Overflow'),
        ('medium', 'Medium'),
        ('other', 'Other'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Social Link"

    def __str__(self):
        return f"{self.get_platform_display()}: {self.url}"


class ContactMessage(models.Model):
    """Messages submitted through the contact form."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"

    def __str__(self):
        return f"{self.name} — {self.subject}"


class SEOSettings(models.Model):
    """SEO settings per page."""
    page_name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=300)
    og_image = models.ImageField(upload_to='seo/', blank=True)
    keywords = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = "SEO Setting"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return f"SEO: {self.page_name}"
