import json

from django.views import View
from django.http  import JsonResponse
from django.db.models import Max, Min

from users.models         import User
from stays.models         import Stay
from wishlists.models     import Wishlist
from utils.login_required import login_required
from utils.convert_price  import convert_price

class WishlistView(View):
    @login_required
    def post(self, request, *args, **kwargs):
        try:
            data    = json.loads(request.body)
            stay_id = data['stayId']
            user    = request.user
            stay = Stay.objects.get(id=stay_id)

            wishlist, is_created = Wishlist.objects.get_or_create(stay=stay, user=user)

            status  = 201
            message = "WISHLIST_IS_CREATED"
            if not is_created:
                wishlist.delete()
                status  = 200
                message = "WISHLIST_IS_DELETED"

            return JsonResponse({"message":message}, status=status)

        except KeyError as e:
            return JsonResponse({"message":getattr(e,"message",str(e))},status=400)

        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status=404)

        except Stay.DoesNotExist:
            return JsonResponse({"message":"STAY_DOES_NOT_EXIST"}, status=404)

    @login_required
    def get(self, request, *args, **kwargs):
        try:
            offset = int(request.GET.get("offset",0))
            limit  = int(request.GET.get("limit",2))

            user      = request.user
            wishlists = Wishlist\
                       .objects\
                       .filter(user=user)\
                       .select_related("stay")\
                       .annotate(min_price=Min('stay__room__roomprice__cost__price'))\
                       .annotate(max_price=Max('stay__room__roomprice__cost__price'))
            
            stays=[
                {
                    "id"          : wish.id,
                    "hotelId"     : wish.stay.id,
                    "hotelNameKor": wish.stay.name,
                    "address"     :f"{wish.stay.state} {wish.stay.city} {wish.stay.address}",
                    "baseNum"     :wish.stay.room_set.first().base_num_people,
                    "maxNum"      :wish.stay.room_set.first().max_num_people,
                    "price"       :f"{convert_price(wish.min_price)} ~ {convert_price(wish.max_price)}",
                    "img"    :wish.stay.thumbnail_url

                    }for wish in wishlists[offset:offset+limit]
            ]

            return JsonResponse({"data":stays}, status = 200)
        except KeyError as e:
            return JsonResponse({"message":getattr(e, "message",str(e))}, status=400)
