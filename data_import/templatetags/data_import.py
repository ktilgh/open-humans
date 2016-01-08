from django import template

from ..utils import app_name_to_user_data_model

register = template.Library()


@register.simple_tag
def source_is_connected(source, user):
    """
    Returns True if the given source is connected (has the required data for
    retrieving the user's data, like a huID or an access token).
    """
    try:
        user_data_model = app_name_to_user_data_model(source)

        user_data = user_data_model.objects.get(user=user)

        return user_data.is_connected
    except:  # pylint: disable=bare-except
        return False
