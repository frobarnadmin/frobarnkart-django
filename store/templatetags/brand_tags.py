from django import template
from store.models import Brand            # ← replace with your app path, e.g. store.models
from accounts.models import Tailor

register = template.Library()

# @register.simple_tag(takes_context=True)
# def my_brand_count(context, active_only: bool = False):
#     """
#     Return the number of Brand rows created by the logged-in tailor.
#     Usage in templates:
#       {% my_brand_count %}            -> all brands
#       {% my_brand_count True %}       -> only active brands
#     """
#     request = context.get("request")
#     user = getattr(request, "user", None)
#
#     if not user or not user.is_authenticated or not getattr(user, "is_tailor", False):
#         return 0
#
#     try:
#         tailor = Tailor.objects.get(account=user)
#     except Tailor.DoesNotExist:
#         return 0
#
#     qs = Brand.objects.filter(brand_company_name=tailor)
#     if active_only:
#         qs = qs.filter(is_active=True)
#     return qs.count()

@register.simple_tag(takes_context=True)
def my_brand_count(context, active_only: bool = False):
    """
    Returns the number of Brand records created by the logged-in tailor.
    Usage:
      {% my_brand_count %}          → all brands
      {% my_brand_count True %}     → only active brands
    """
    request = context.get("request")
    user = getattr(request, "user", None)

    if not user or not user.is_authenticated or not getattr(user, "is_tailor", False):
        return 0

    try:
        tailor = Tailor.objects.get(account=user)
    except Tailor.DoesNotExist:
        return 0

    qs = Brand.objects.filter(brand_company_name=tailor)
    if active_only:
        qs = qs.filter(is_active=True)
    return qs.count()