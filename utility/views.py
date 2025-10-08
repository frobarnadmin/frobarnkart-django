from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, NewsletterContact
from django.http import JsonResponse
from django.urls import reverse
from .forms import NewsletterForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect("contact")  # named URL defined below
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ContactForm()

    return render(request, "utility/contact.html", {"form": form})

def _send_thank_you_email(to_email: str, source: str = "popup"):
    """
    Sends a simple thank-you email to the subscriber.
    Looks for optional templates:
      - templates/emails/newsletter_thanks.html
      - templates/emails/newsletter_thanks.txt
    Falls back to a minimal inline message if templates are missing.
    """
    subject = "Thanks for subscribing!"
    brand = getattr(settings, "SITE_NAME", "Our Store")

    # Try to render templates; fall back if not present
    try:
        html_body = render_to_string(
            "emails/newsletter_thanks.html",
            {"brand": brand, "source": source}
        )
    except Exception:
        html_body = (
            f"<p>Hi there,</p>"
            f"<p>Thanks for subscribing to {brand}! "
            f"We'll keep you posted with updates and offers.</p>"
            f"<p>— {brand} Team</p>"
        )

    try:
        text_body = render_to_string(
            "emails/newsletter_thanks.txt",
            {"brand": brand, "source": source}
        )
    except Exception:
        text_body = strip_tags(html_body)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_body, "text/html")
    # Fail silently so subscription never errors due to email issues
    msg.send(fail_silently=True)


def subscribe_newsletter(request):
    if request.method != "POST":
        return redirect("/")

    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]

        # Determine the source: from form field, query param, or fallback
        source = request.POST.get("source") or request.GET.get("source") or "unknown"

        # Save or update contact
        obj, created = NewsletterContact.objects.get_or_create(
            email=email,
            defaults={"source": source},
        )

        # Update the source if missing
        if not created and not obj.source and source:
            obj.source = source
            obj.save(update_fields=["source"])

        # Send thank-you email only for new signups
        if created:
            _send_thank_you_email(email, source)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "created": created})

        messages.success(request, "Thanks for subscribing!")
        return redirect(request.META.get("HTTP_REFERER", reverse("home")))

    # If invalid
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    messages.error(request, "Please enter a valid email.")
    return redirect(request.META.get("HTTP_REFERER", reverse("home")))

# from django.http import JsonResponse
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.contrib import messages
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# from .forms import NewsletterForm
# from .models import NewsletterContact

