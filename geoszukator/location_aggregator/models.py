from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Continents(models.Model):
    continent_name = models.CharField(max_length=64, unique=True)
    continent_code =  models.CharField(max_length=5)
    
    def __str__(self):
        return self

class Languages(models.Model):
    language = models.CharField(max_length=255, unique=True)
    language_code = models.CharField(max_length=5)

    def __str__(self):
        return self

class Flags(models.Model):
    flag = models.CharField(max_length=64) 
    flag_emoji = models.ImageField(upload_to='flags')
    flag_emoji_unicode = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self

class Countries(models.Model):
    country_name = models.CharField(max_length=255, unique=True)
    country_code = models.CharField(max_length=5)
    capital = models.CharField(max_length=255)
    country_flag = models.ForeignKey(Flags, on_delete=models.CASCADE, related_name="flags")
    continent = models.ForeignKey(Continents, on_delete=models.CASCADE, related_name="continents")
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name="languages")
    calling_code = models.CharField(max_length=10)
    is_eu = models.BooleanField()

    def __str__(self):
        return self

class Regions(models.Model):
    region_name = models.CharField(max_length=255, unique=True)
    region_code = models.CharField(max_length=5)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name="countries")

    def __str__(self):
        return self
class Cities(models.Model):
    city_name = models.CharField(max_length=255)
    zip_value = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=20, decimal_places=10)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)
    ip_code = models.CharField(max_length=24, unique=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name="regions")

    def __str__(self):
        return self


