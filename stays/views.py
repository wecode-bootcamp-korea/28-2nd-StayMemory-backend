from django.core.exceptions       import FieldError
from json.decoder                 import JSONDecodeError
from django.http                  import JsonResponse

from django.db.models.aggregates  import Max,Min
from django.db.models.query_utils import Q

from django.views                 import View
from stays.models                 import Stay
from utils.convert_price          import convert_price
from utils.check_weekday          import include_weekday_boolean

class StayListView(View):
    def get(self, request):
        try:
            city_name      = request.GET.get('city', None)
            check_in       = request.GET.get('checkin', None)
            check_out      = request.GET.get('checkout', None)
            room_min_price = request.GET.get('minprice', 10000)
            room_max_price = request.GET.get('maxprice', None)
            category       = request.GET.get('category', None)
            max_num_people = request.GET.get('adult', None)            
            sorts          = request.GET.get('sort','id')

            q=Q()
            
            if city_name:
                q &= Q(state=city_name)

            if category:
                q &= Q(category__name=category)

            if max_num_people:
                q &= Q(max_people__gte=max_num_people)
                
            if room_max_price:
                q &= Q(price__lte=int(room_max_price))
                
            if room_min_price:
                q &= Q(price__gte=int(room_min_price))

            stays = Stay.objects.all()
            
            stays = stays.annotate(price=Min('room__roomprice__cost__price'))

            if check_in and check_out:
                if not include_weekday_boolean(check_in, check_out):
                    stays = stays.annotate(price=Max('room__roomprice__cost__price'))
            
            stays = stays.annotate(max_people=Max('room__max_num_people'), base_people=Max('room__base_num_people'),\
                                   min_price=Min('room__roomprice__cost__price'), max_price=Max('room__roomprice__cost__price'))\
                                   .filter(q).order_by(sorts)
            
            if check_in and check_out:
                stays = stays.exclude(room__reservation__check_in_date__gt=check_out, room__reservation__check_out_date__lt=check_in)

            result = [{
                'id'           : stay.id,
                'hotelNameKor' : stay.name,
                'price'        : f"{convert_price(stay.min_price)} ~ {convert_price(stay.max_price)}",
                'baseNum'      : stay.base_people,
                'maxNum'       : stay.max_people,
                'stayType'     : stay.category.name,
                'img'          : stay.thumbnail_url,
            }for stay in stays]

            return JsonResponse({'data' : result}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEYERROR'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except FieldError:
            return JsonResponse({'message' : 'Bad_Request'}, status=404)