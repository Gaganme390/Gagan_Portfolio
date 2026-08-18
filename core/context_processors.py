from .models import Profile, SocialLink


def global_context(request):
    """Provide profile and social links to all templates."""
    return {
        'global_profile': Profile.objects.first(),
        'global_social_links': SocialLink.objects.filter(is_visible=True),
    }
