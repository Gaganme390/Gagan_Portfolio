from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Profile, Skill, Experience, Project,
    Certification, Education, SocialLink, ContactMessage
)
import json


def index(request):
    """Main portfolio page with all sections."""
    profile = Profile.objects.first()
    skills_by_category = {}
    for skill in Skill.objects.filter(is_featured=True):
        cat = skill.get_category_display()
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill)

    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'experiences': Experience.objects.all(),
        'projects': Project.objects.filter(is_featured=True),
        'certifications': Certification.objects.all(),
        'education': Education.objects.all(),
        'social_links': SocialLink.objects.filter(is_visible=True),
    }
    return render(request, 'index.html', context)


def project_detail(request, slug):
    """Individual project showcase page."""
    project = get_object_or_404(Project, slug=slug)
    other_projects = Project.objects.filter(is_featured=True).exclude(id=project.id)[:3]
    context = {
        'project': project,
        'screenshots': project.screenshots.all(),
        'other_projects': other_projects,
    }
    return render(request, 'projects/detail.html', context)


def download_resume(request):
    """Serve the resume PDF for download."""
    profile = Profile.objects.first()
    if profile and profile.resume_file:
        return FileResponse(
            profile.resume_file.open('rb'),
            as_attachment=True,
            filename='Gagan_Sahu_Resume.pdf'
        )
    return JsonResponse({'error': 'Resume not available'}, status=404)


@csrf_exempt
@require_POST
def contact_submit(request):
    """Handle contact form submission via AJAX."""
    try:
        data = json.loads(request.body)
        msg = ContactMessage.objects.create(
            name=data.get('name', ''),
            email=data.get('email', ''),
            subject=data.get('subject', ''),
            message=data.get('message', ''),
        )
        return JsonResponse({
            'success': True,
            'message': 'Thank you for reaching out! I will get back to you soon.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
