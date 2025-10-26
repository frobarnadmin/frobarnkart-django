# accounts/templatetags/form_extras.py
from django import template

register = template.Library()

@register.filter
def add_class(field, has_errors):
    current = field.field.widget.attrs.get("class", "")
    if has_errors:
        field.field.widget.attrs["class"] = (current + " is-invalid").strip()
    return field

