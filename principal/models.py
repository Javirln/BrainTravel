# -*- coding: latin-1 -*-
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


# --------------------------- CUSTOMS VALIDATORS  ----------------------------------
def PastValidator(value):
    if value > timezone.now():
        raise ValidationError(u'' + str(value) + ' Is a future date!')
# -----------------------------------------------------------------------------------


# Create your models here.


class Actor(models.Model):
    user_account = models.OneToOneField(User)
    
    class Meta:
        abstract = True;


class Administrator(Actor):
    class Meta:
        permissions = (
                       ('administrator', 'Administrator'),
                       )
        db_table = 'administrator'

class Category(models.Model):
    id_foursquare = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)
    
    
    class Meta:
        db_table = 'category'
    
    def __unicode__(self):
        return self.name 


# Conceptually it's abstract, but Django not implement in BD abstract classes
class Scorable(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    
    #----------- Derivates -------------------------------#
    rating = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        db_table = 'scorable'
    
class Venue(Scorable):
    id_foursquare = models.CharField(max_length=30, unique=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='static/venue_folder/', null=True, blank=True)
    phone = models.CharField(max_length=50, null=True)
    
    # ------------- Relationships --------------#
    categories = models.ManyToManyField(Category)
    
    class Meta:
        db_table = 'venue'
        
    def __unicode__(self):
        return self.name


class Feedback(models.Model):
    description = models.TextField(null=True)
    leadTime = models.FloatField(validators=[MinValueValidator(1)])
    duration = models.FloatField(validators=[MinValueValidator(1)])
    
    #---------- Derivate ---------------#
    usefulCount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # ------------- Relationships --------------#
    traveller = models.ForeignKey('principal.Traveller')
    venues = models.ForeignKey(Venue)
    
    class Meta:
        db_table = 'feedback'
    
    def __unicode__(self):
        return self.description
    
class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        db_table = 'city'
    
    def __unicode__(self):
        return self.name

class Trip(Scorable):
    publishedDescription = models.TextField(null=True)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    planified = models.BooleanField(default=False)
    coins = models.IntegerField(validators=[MinValueValidator(0)])
    
    #------------- Derivates -----------------------------#
    likes = models.IntegerField(validators=[MinValueValidator(0)])
    dislikes = models.IntegerField(validators=[MinValueValidator(0)])
    
    # ------------- Relationships --------------#
    traveller = models.ForeignKey('principal.Traveller')
    city = models.ForeignKey(City)
    
    class Meta:
        db_table = 'trip'
    
    def __unicode__(self):
        return 'Ini: ' + self.startDate + 'End: ' + self.endDate

class Traveller(Actor):
    
    Genre = (
             ('MA', 'MALE'),
             ('FE', 'FEMALE')
             )
    
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    genre = models.CharField(max_length=2, choices=Genre)
    photo = models.ImageField(upload_to='static/user_folder/', null=True, blank=True)
    
    # ----------- Derivates -------------------#
    reputation = models.FloatField(null=True, blank=True,
            validators=[MinValueValidator(0), MaxValueValidator(10)])
    coins = models.IntegerField(validators=[MinValueValidator(0)])
    recommendations = models.IntegerField(validators=[MinValueValidator(0)])
    
    # ------------- Relationships --------------#
    likedFeedback = models.ManyToManyField(Feedback, through='Likes', related_name='traveller_likes')
    jugedTrips = models.ManyToManyField(Trip, through='Judges', related_name='judges')
    commentedTrips = models.ManyToManyField(Trip, through='Comment', related_name='commenters')
    assessedScorables = models.ManyToManyField(Scorable, through='Assessment')
    
    class Meta:
        db_table = 'traveller'
        permissions = (
                       ('traveller', 'Traveller'),
                       )
    
    def __unicode__(self):
        return self.firstName + ' ' + self.lastName


class Likes(models.Model):
    useful = models.BooleanField(default=False)
    comment = models.TextField(null=True)
    
    #-------------- Relationships -------------------
    traveller = models.ForeignKey(Traveller)
    feedback = models.ForeignKey(Feedback)
    
    class Meta:
        db_table = 'likes'
    
    
class Day(models.Model):
    numberDay = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField(null=True)
    description = models.TextField(null=True)
    
    # ------------- Relationships --------------#
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    venues = models.ManyToManyField(Venue, through='VenueDay')
    
    class Meta:
        db_table = 'day'
    
    def clean(self):
        if self in self.trip.day_set:
            raise ValidationError('The trip already contains this day!')
    
class VenueDay(models.Model):
    order = models.IntegerField(validators=[MinValueValidator(1)])
    
    # ------------- Relationships --------------#
    venue = models.ForeignKey(Venue)
    day = models.ForeignKey(Day)
    
    class Meta:
        unique_together = ('venue', 'day')
        db_table = 'venue_day'
    
    
class Comment(models.Model):
    description = models.TextField()
    
    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    trip = models.ForeignKey(Trip)
    class Meta:
        db_table = 'comment'
    
class Judges(models.Model):
    like = models.BooleanField(default=False)
    
    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    trip = models.ForeignKey(Trip, related_name='judgedTrip')
    
    class Meta:
        db_table = 'judges'


class Payment(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(validators=[PastValidator])
    
    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    
    class Meta:
        db_table = 'payment'

class CoinHistory(models.Model):
    amount = models.IntegerField()
    date = models.DateTimeField(validators=[PastValidator])
    concept = models.TextField()
    
    # -------------     Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    payment = models.OneToOneField(Payment, null=True, blank=True) 
    trip = models.OneToOneField(Trip, null=True, blank=True)
    
    class Meta:
        db_table = 'coin_history'
    
    def __unicode__(self):
        return str(self.amount)
    


class Schedule(models.Model):
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    openingTime = models.CharField(null=True, max_length=128)
    closingTime = models.CharField(null=True, max_length=128)
    
    # ------------- Relationships --------------#
    venue = models.ForeignKey(Venue)
    
    class Meta:
        db_table = 'schedule'
            
class Assessment(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    comment = models.TextField()
    
    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    scorable = models.ForeignKey(Scorable)
    
    class Meta:
        db_table = 'assessment'