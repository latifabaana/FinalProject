from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from django.core.validators import MinLengthValidator

User = get_user_model()

def upload_path(instance, filename):
    return '/'.join(['uploads/areaimg', filename])
    
class Area(models.Model):
    name = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value = 4, message="Too short")], null=False, blank=False)
    country = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value = 4, message="Too short")], null=False, blank=False) 
    city= models.CharField(max_length=30, null=False, blank=False) 
    borough = models.CharField(max_length=30, null=False, blank=False) 
    image = models.ImageField(upload_to='uploads/areaimg', default= 'uploads/areaimg/default.png', null = True, blank = True )
    homeless_sightings = models.IntegerField(default = 0, blank=True)
    litter_count = models.IntegerField(default =0, blank=True)
    swearing_count =models.IntegerField(default=0, blank=True)
    cig_but_count = models.IntegerField(default=0, blank=True)

    # increment ratings
    def process_rating(self, rating):
        if rating == 'homeless_sightings':
            self.homeless_sightings += 1
        elif rating == 'litter_count':
            self.litter_count += 1
        elif rating == 'swearing_count':
            self.swearing_count += 1
        elif rating == 'cig_but_count':
            self.cig_but_count += 1
        else:
            print('process_rating is not successful')

    # delete ratings
    def delete_rating(self, rating):
        if rating == 'homeless_sightings':
            self.homeless_sightings -= 1
        elif rating == 'litter_count':
            self.litter_count -= 1
        elif rating == 'swearing_count':
            self.swearing_count -= 1
        elif rating == 'cig_but_count':
            self.cig_but_count -= 1
        else:
            print('process_rating is not successful')

    def _str__(self):
        return self.name


class Rating(models.Model):
    area = models.ForeignKey(Area, related_name='rating_item', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=False, blank=False)  

    def _str__(self):
        return self.area.name
