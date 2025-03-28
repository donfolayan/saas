from django.db import models
from django.conf import settings
import helpers.billing

User = settings.AUTH_USER_MODEL

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.stripe_id}'
    
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            email = self.user.email
            if email != '' or email is not None:
                stripe_id = helpers.billing.create_customer(email=email, raw=False)
                self.stripe_id = stripe_id
        super().save(*args, **kwargs)