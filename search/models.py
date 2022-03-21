# from adaptor.model import CsvModel
# from adaptor.fields import CharField, IntegerField, BooleanField, FloatField
from django.db import models
from django.contrib import admin

class Paper(models.Model):

    conference = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    abstract= models.CharField(max_length=5000)
    keywords= models.CharField(max_length=1000)
    citations = models.IntegerField()


    def __str__(self):
        return self.title


    @admin.display(description='Number of authiors')
    def author_numbers(self):
        authors = self.authors
        author_list = authors.split(',')
        return len(author_list)


    @admin.display(description='First author')
    def first_author(self):
        authors = self.authors
        author_list = authors.split(',')
        return author_list[0]
