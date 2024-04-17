from django.db import models
from authentication.models import User
# Create your models here.
class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=500, null=False)
    budget = models.IntegerField()
    season = models.CharField(max_length=255, null=False)
    date = models.DateField()
    guests = models.IntegerField()

    def __str__(self):
        return "{} -{}, {}, {}".format(self.user, self.location, self.budget, self.season)

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{}, {}".format(self.user, self.name)

class ItineraryItem(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    location = models.CharField(max_length=500, null=False)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()
    item_name = models.CharField(max_length=255, null=False)
    item_description = models.TextField()
    item_type = models.CharField(max_length=255, null=False)
    notes = models.TextField()

    def __str__(self):
        return "{} -{}".format(self.itinerary, self.item_name)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    date = models.DateField()

    def __str__(self):
        return "{} -{} {}".format(self.itinerary, self.rating,self.user)