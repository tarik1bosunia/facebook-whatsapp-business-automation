from django.core.exceptions import ValidationError
from messaging.models import SocialMediaUser


def get_or_create_user(social_media_id, platform=None, name=None, avatar_url=None, customer=None):
    """
    Get or create a SocialMediaUser with the given social_media_id.

    Args:
        social_media_id (str): The unique ID from the social platform
        platform (str, optional): The social platform (e.g., 'facebook', 'whatsapp')
        name (str, optional): The user's display name
        avatar_url (str, optional): URL to the user's avatar/image
        customer (Customer, optional): Associated Customer object

    Returns:
        tuple: (SocialMediaUser instance, created: bool)

    Raises:
        ValidationError: If social_media_id is not provided or invalid
    """
    if not social_media_id:
        raise ValidationError("social_media_id is required")

    defaults = {}
    if name:
        defaults['name'] = name
    else:
        defaults['name'] = f"User {social_media_id[:8]}..."  # Truncate long IDs

    if platform:
        defaults['platform'] = platform

    if avatar_url:
        defaults['avatar_url'] = avatar_url

    if customer:
        defaults['customer'] = customer

    try:
        user, _ = SocialMediaUser.objects.get_or_create(
            social_media_id=social_media_id,
            defaults=defaults
        )
        return user
    except Exception as e:
        # Handle cases where the same social_media_id exists with different platform
        existing_user = SocialMediaUser.objects.filter(social_media_id=social_media_id).first()
        if existing_user:
            # Update fields if provided
            update_fields = []
            if name and existing_user.name != name:
                existing_user.name = name
                update_fields.append('name')
            if avatar_url and existing_user.avatar_url != avatar_url:
                existing_user.avatar_url = avatar_url
                update_fields.append('avatar_url')
            if customer and existing_user.customer != customer:
                existing_user.customer = customer
                update_fields.append('customer')

            if update_fields:
                existing_user.save(update_fields=update_fields)
            return existing_user, False

        raise ValidationError(f"Failed to get or create user: {str(e)}")