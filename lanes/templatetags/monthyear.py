from django import template
import datetime

register = template.Library()

@register.filter
def monthyear(value):
    """
    Converts 'YYYY-MM' → 'Jan 2026'
    """
    if not value:
        return ""
    try:
        date_obj = datetime.datetime.strptime(value, "%Y-%m")
        return date_obj.strftime("%b %Y")
    except ValueError:
        return value