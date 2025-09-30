from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, **kwargs):
    """
    Replace URL parameters while preserving existing ones.
    Usage: {% url_replace request page=2 %}
    """
    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()
