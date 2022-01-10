import uuid

from django.db import models

from utils.time_stamp_model import TimeStampModel
from users.models           import User
from stays.models           import Room

class ReservationStatus(models.Model):
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "reservation_statuses"

class Payment(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "payments"

class Reservation(TimeStampModel):
    user               = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room               = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    reservation_status = models.ForeignKey(ReservationStatus, on_delete=models.SET_NULL, null=True)
    check_in_date      = models.DateTimeField()
    check_out_date     = models.DateTimeField()
    reservation_number = models.UUIDField(default=uuid.uuid4)
    payment_id         = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    price              = models.DecimalField(max_digits=12, decimal_places=2)
    num_people         = models.IntegerField()

    class Meta:
        db_table = "reservations"

