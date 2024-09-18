from django.db import models

from base.models import BaseModel

class Author(BaseModel):
    name = models.CharField("Name", max_length=255,null=False,blank=False)
    gender = models.CharField("Gender", max_length=55,null=True,blank=True)
    image_url = models.CharField("Image URL", max_length=55,null=True,blank=True)
    about = models.TextField("About", null=True,blank=True)
    reviews_count = models.IntegerField("Reviews Count",null=False,default=0)
    fans_count = models.IntegerField("Fans Count",null=False,default=0)
    ratings_count = models.IntegerField("Rating Count",null=False,default=0)
    average_rating = models.DecimalField("Average Rating",null=False,default=0,decimal_places=2,max_digits=3)

