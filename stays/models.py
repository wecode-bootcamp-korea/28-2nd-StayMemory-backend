from django.db import models

from users.models  import User
from admins.models import Admin

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "categories"

class Stay(models.Model):
    name            = models.CharField(max_length=50)
    expression      = models.CharField(max_length=100)
    description     = models.TextField()
    city            = models.CharField(max_length=30)
    state           = models.CharField(max_length=30)
    address         = models.CharField(max_length=100)
    thumbnail_url   = models.URLField(max_length=1000)
    description_url = models.URLField(max_length=1000)
    launched_at     = models.DateTimeField()
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    admin           = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "stays"

class StayImage(models.Model):
    image_url = models.URLField(max_length=1000)
    stay      = models.ForeignKey(Stay, on_delete=models.CASCADE)

    class Meta:
        db_table = "stay_images"

class Room(models.Model):
    stay             = models.ForeignKey(Stay, on_delete=models.CASCADE)
    name             = models.CharField(max_length=50)
    room_description = models.TextField()
    check_in_time    = models.CharField(max_length=30)  
    check_out_time   = models.CharField(max_length=30)
    base_num_people  = models.IntegerField()
    max_num_people   = models.IntegerField()
    area             = models.DecimalField(max_digits=10, decimal_places=3)
    queen_bed        = models.IntegerField()
    single_bed       = models.IntegerField()
    double_bed       = models.IntegerField()
    policy           = models.TextField()

    class Meta:
        db_table = "rooms"

class RoomImage(models.Model):
    room      = models.ForeignKey(Room, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000)

    class Meta:
        db_table = "room_images"

class Cost(models.Model):
    price            = models.DecimalField(max_digits=12, decimal_places=2)
    additional_price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_basis       = models.CharField(max_length=50)

    class Meta:
        db_table = "cost"

class RoomPrice(models.Model):
    room  = models.ForeignKey(Room, on_delete=models.CASCADE)
    cost  = models.ForeignKey(Cost, on_delete=models.CASCADE)

    class Meta:
        db_table = "room_price"
