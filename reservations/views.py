import json
import uuid

from datetime         import datetime
from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from utils.login_required import login_required
from reservations.models  import (Reservation,
                                  Payment,
                                  ReservationStatus)
from users.models         import User
from stays.models         import Room

class ReservationInformationView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        try:
            category = request.GET["filter"]
            offset   = int(request.GET.get("offset", 0))
            limit    = int(request.GET.get("limit", 2))
            user     = request.user

            q = Q(user=user)
            today = datetime.today().strftime("%Y-%m-%d")
            if category == "reservation":
                q &= Q(check_in_date__gte=today)
            if category == "history":
                q &= Q(check_in_date__lt=today)

            user = request.user
            reservations = Reservation.objects.filter(user=user)

            data = [{
                "reservationId"    : res.id,
                "reservationNumber": res.reservation_number,
                "hotelName"        : res.room.stay.name,
                "hotelId"          : res.room.stay.id,
                "address"          : f"{res.room.stay.state} {res.room.stay.city} {res.room.stay.address}",
                "baseNum"          : res.room.base_num_people,
                "maxNum"           : res.room.max_num_people,
                "checkInDate"      : res.check_in_date.strftime("%Y-%m-%d"),
                "checkOutDate"     : res.check_out_date.strftime("%Y-%m-%d"),
                "price"            : int(res.price),
                "img"              : res.room.stay.thumbnail_url,
            }for res in reservations[offset:offset+limit]]

            return JsonResponse({"data":data}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    @login_required
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user

            stay_id        = data["stayId"]
            num_people     = data["numPeople"]
            checkin        = data["checkin"]
            checkout       = data["checkout"]
            price          = data["price"]
            payment_method = data["payment"]

            reservations = Reservation.objects.filter(
                    user           = user, 
                    check_in_date  = checkin,
                    check_out_date = checkout,
            )
            if reservations:
                return JsonResponse({"message":"DUPLICATED_RESERVATION"}, status=400)

            payments = Payment.objects.all()

            payment = Payment.objects.get(name=payment_method)
            status  = ReservationStatus.objects.get(status="complete")
            room    = Room.objects.get(stay_id=stay_id)

            reservation = Reservation.objects.create(
                user               = user,
                room               = room,
                reservation_status = status,
                check_in_date      = checkin,
                check_out_date     = checkout,
                reservation_number = uuid.uuid4(),
                payment_id         = payment,
                price              = price,
                num_people         = num_people,
            )

            return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except Payment.DoesNotExist:
            return JsonResponse({"message":"WRONG_PAYMENT_METHOD"}, status=400)

        except ReservationStatus.DoesNotExist:
            return JsonResponse({"message":"RESERVATIONSTATUS_DOES_NOT_EXIST"}, status=400)

        except Room.DoesNotExist:
            return JsonResponse({"message":"ROOM_DOES_NOT_EXIST"}, status=404)
