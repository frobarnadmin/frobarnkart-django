from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

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