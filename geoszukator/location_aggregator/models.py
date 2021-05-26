from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Continents(models.Model):
    continent_name = models.CharField(max_length=64)
    continent_code =  models.CharField(max_length=5)
    
    def __str__(self):
        return f"{self.id}: {self.continent_name}"

class Languages(models.Model):
    language = models.CharField(max_length=255)
    language_code = models.CharField(max_length=5)

class Flags(models.Model):
    flag = models.CharField(max_length=64) 
    flag_emoji = models.ImageField(upload_to='flags')
    flag_emoji_unicode = models.CharField(max_length=64)

class Countries(models.Model):
    country_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=5)
    capital = models.CharField(max_length=255)
    country_flag_id = models.ForeignKey(Flags, on_delete=models.CASCADE, related_name="Flags")
    continent_id = models.ForeignKey(Continents, on_delete=models.CASCADE, related_name="Continents")
    language_id = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name="Languages")
    native_id = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name="Native")
    calling_code = models.IntegerField()
    is_eu = models.BooleanField()

class Regions(models.Model):
    region_name = models.CharField(max_length=255)
    region_code = models.CharField(max_length=5)
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name="Countries")

class Cities(models.Model):
    city_name = models.CharField(max_length=255)
    zip = models.IntegerField()
    latitude = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)
    region_id = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name="Regions")




