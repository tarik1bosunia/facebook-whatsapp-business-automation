from ..models import SocialMediaUser

def get_or_create_user(social_media_id):
    user, created = SocialMediaUser.objects.get_or_create(
        social_media_id=social_media_id,
        defaults={'name': f"User {social_media_id}"}
    )
    return user