from django.db import models
# Create your models here.
from django.template.defaultfilters import slugify

class Category(models.Model):
        name = models.CharField(max_length=128, unique=True)
        views = models.IntegerField(default=0)
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

class Game(models.Model):
    category = models.ForeignKey(Category)
    gameID= models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=128)
    views = models.IntegerField(default=0)#
    server = models.CharField(max_length=128, default = "World")
    platform = models.CharField(max_length=128, default = "PC")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            self.slug = slugify(self.gameID)
            super(Game, self).save(*args, **kwargs)
    def __unicode__(self):      #For Python 2, use __str__ on Python 
        return self.name
		
class Thread(models.Model):
    game = models.ForeignKey(Game)
    title = models.CharField(max_length=128)
    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title