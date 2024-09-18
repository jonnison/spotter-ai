from django.db import models
from base.models import BaseModel
from authors.models import Author


 

class Book(BaseModel):
    name = models.CharField("Name", max_length=255,null=False,blank=False)
    isbn = models.CharField("ISBN", max_length=55,null=True,blank=True)
    isbn13 = models.CharField("ISBN13", max_length=55,null=True,blank=True)
    language = models.CharField("Language", max_length=55,null=True,blank=True)
    publisher = models.CharField("Publisher", max_length=255,null=True,blank=True)
    publication_date = models.DateField("Publication Date", null=True)
    format = models.CharField("Format", max_length=55,null=True,blank=True)
    series_name = models.CharField("Series Name", max_length=255,null=True,blank=True)
    series_position = models.CharField("Series Position", max_length=55,null=True,blank=True)
    language = models.CharField("Language", max_length=55,null=True,blank=True)
    image_url = models.CharField("Image URL", max_length=55,null=True,blank=True)
    about = models.TextField("About", null=True,blank=True)
    reviews_count = models.IntegerField("Reviews Count",null=False,default=0)
    fans_count = models.IntegerField("Fans Count",null=False,default=0)
    ratings_count = models.IntegerField("Rating Count",null=False,default=0)
    average_rating = models.DecimalField("Average Rating",null=False,default=0,decimal_places=2,max_digits=3)
    authors = models.ManyToManyField(Author, through='AuthorBook')

class AuthorBook(BaseModel):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    role =  models.CharField("Role", max_length=55,null=True,blank=True)