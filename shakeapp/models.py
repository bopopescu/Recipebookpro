__author__ = "Keith Lee"
__email__ = "keithlee002@gmail.com"

from django.db import models
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
        print instance
        return "recipePictures/{name}/{file}".format(name=instance.name, file=filename)

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to=get_upload_path)
    url = models.URLField()
    ingredients = models.TextField()
    instruction = models.TextField()
    numLikes = models.IntegerField(default=0)
    cookHour= models.IntegerField(default=0)
    cookMin= models.IntegerField(default=0)
    def __unicode__(self):
        return u"Recipe(%s, %s, %s, %s, %s, %d, %d, %d)" % (self.name, self.picture,self.url, self.ingredients, self.instruction, self.numLikes, self.cookHour, self.cookMin)

# Table to keep track of the recipes that each user likes.
# Had to include username and recipeName fields to work with non-relational DB.    
class RecipeLikes(models.Model):
    user = models.ForeignKey(User) 
    recipe = models.ForeignKey('Recipe')
    def __unicode__(self):
        return u"likes(%s, %s)" % (self.user, self.recipe)

