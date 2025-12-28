"""
Custom template tags for maintenance app.

🔍 EXPLANATION FOR BEGINNERS:
Template tags allow you to create custom functions that can be used in templates.
This filter helps access dictionary values in templates.
"""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    🔍 EXPLANATION: get_item filter
    Gets a value from a dictionary using a key.
    
    Usage in template:
    {{ requests_by_status|get_item:"New" }}
    
    This is needed because Django templates don't support dictionary[key] syntax.
    """
    if dictionary is None:
        return []
    return dictionary.get(key, [])

