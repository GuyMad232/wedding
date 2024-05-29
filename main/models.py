from django.db import models

class GuestList(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the guest list or event.")
    description = models.TextField(blank=True, help_text="Description of the guest list or event.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Guest(models.Model):
    guest_list = models.ForeignKey(GuestList, on_delete=models.CASCADE, related_name="guests")
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    attending = models.BooleanField(blank=True, null=True)  # Allow NULL values
    number_of_guests_invited = models.IntegerField(default=0)
    number_of_guests_attending = models.IntegerField(default=0)
    message = models.TextField(blank=True, null=True)  # Allow NULL values
    email_sent = models.BooleanField(default=False)  # New field
    identification = models.IntegerField(unique=True, null=True, blank=True)  # New field

    def __str__(self):
        return self.name
    
    def attending_guests(self):
        """Return a queryset of guests who have confirmed attendance."""
        return self.guests.filter(self.attending == True)
