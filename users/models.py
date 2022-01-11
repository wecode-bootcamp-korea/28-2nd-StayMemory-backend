from django.db import models

from utils.time_stamp_model import TimeStampModel

class User(TimeStampModel):
    kakao_id = models.CharField(max_length=25, unique=True)
    nickname = models.CharField(max_length=50)
    email    = models.CharField(max_length=30)
    gender   = models.IntegerField()

    class Meta:
        db_table = "users"
