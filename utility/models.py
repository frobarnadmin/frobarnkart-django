from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=80)
    last_name  = models.CharField(max_length=80, blank=True)
    phone      = models.CharField(max_length=40, blank=True)
    email      = models.EmailField()
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()