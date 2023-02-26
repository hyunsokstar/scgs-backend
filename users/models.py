from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMAIL = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korea")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    name = models.CharField(max_length=150, default="")
    profile_image = models.URLField(blank=True, null=True)    
    gender = models.CharField(max_length=10, choices=GenderChoices.choices,)
    # is_host = models.BooleanField(default=False)
    # language = models.CharField(max_length=2, choices=LanguageChoices.choices, null=True, blank=True)
    # currency = models.CharField(max_length=5, choices=CurrencyChoices.choices,)