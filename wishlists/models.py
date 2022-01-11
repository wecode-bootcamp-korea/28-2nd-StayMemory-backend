from django.db import models

from utils.time_stamp_model import TimeStampModel
from users.models           import User
from stays.models           import Stay

class Wishlist(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)

    class Meta:
        db_table = "wishlists"
