from django.contrib import admin
from .models import (
    Profile, Skill, Experience, Project, ProjectScreenshot,
    Certification, Education, SocialLink, ContactMessage, SEOSettings
)


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'title', 'email', 'phone', 'location')
        }),
        ('Online Presence', {
            'fields': ('linkedin', 'github', 'website')
        }),
        ('Hero Section', {
            'fields': ('hero_tagline', 'hero_subtitles', 'professional_summary')
        }),
        ('About Me', {
            'fields': ('about_me',)
        }),
        ('Statistics', {
            'fields': ('years_experience', 'projects_completed', 'certifications_count')
        }),
        ('Media', {
            'fields': ('profile_image', 'resume_file')
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
    )
    list_display = ['full_name', 'title', 'email', 'updated_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    list_editable = ['proficiency', 'is_featured', 'order']
    search_fields = ['name']
    ordering = ['category', 'order']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['is_current', 'company']
    list_editable = ['order']
    search_fields = ['title', 'company']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'role', 'is_featured', 'order', 'updated_at']
    list_filter = ['is_featured']
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectScreenshotInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'tagline', 'role', 'accent_color')
        }),
        ('Content', {
            'fields': ('overview', 'problem_statement', 'features', 'challenges',
                       'architecture', 'lessons_learned')
        }),
        ('Technologies', {
            'fields': ('technologies',)
        }),
        ('Links', {
            'fields': ('github_link', 'demo_link')
        }),
        ('Media', {
            'fields': ('hero_image', 'thumbnail')
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'category', 'date_earned', 'order']
    list_filter = ['category', 'issuer']
    list_editable = ['order']
    search_fields = ['name']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'graduation_year', 'gpa', 'order']
    list_editable = ['order']
    search_fields = ['degree', 'institution']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_visible', 'order']
    list_editable = ['is_visible', 'order']
    list_filter = ['platform', 'is_visible']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']

    def has_add_permission(self, request):
        return False


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'title']
    search_fields = ['page_name', 'title']
