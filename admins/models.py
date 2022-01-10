from django.db import models

from utils.time_stamp_model import TimeStampModel

class Admin(TimeStampModel):
    name     = models.CharField(max_length=30)
    admin_id = models.CharField(max_length=30)
    password = models.CharField(max_length=256)
    email    = models.CharField(max_length=100)

    class Meta:
        db_table = "admins"

