from django.core.exceptions       import FieldError
from json.decoder                 import JSONDecodeError
from django.http                  import JsonResponse

from django.db.models.aggregates  import Max,Min
from django.db.models.query_utils import Q

import datetime
from django.views                 import View

from stays.models                 import Stay

class StayListView(View):
    def checking_date(start_date, end_date):
        check_in_date  = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
        days = (check_in_date-check_out_date).days

        if days >= 4:
            return True

        weekend       = {4,5,6}

        weekdays = {(check_in_date+datetime.timedelta(days=i)).weekday() for i in range(days)}
        if weekdays&weekend:
            return True

        return False


    def get(self, request):
        try:
            city_name      = request.GET.get('city', None)
            check_in       = request.GET.get('check_in_date', None)
            check_out      = request.GET.get('check_out_date', None)
            room_min_price = request.GET.get('min_price', 10000)
            room_max_price = request.GET.get('max_price', None)
            category       = request.GET.get('category', None)
            sorts          = request.GET.get('sort','id')
            max_num_people = request.GET.get('max_people', None)

            q=Q()

            if city_name:
                q &= Q(state=city_name)
            if category:
                q &= Q(category__name=category)
            if max_num_people:
                q &= Q(max_people__gte=max_num_people)
            if room_min_price:
                q &= Q(price__gte=int(room_min_price))
            if room_max_price:
                q &= Q(price__lte=int(room_max_price))

            print(q)
            stays = Stay.objects.annotate(max_people=Max('room__max_num_people'),base_people=Max('room__base_num_people')).filter(q).order_by(sorts)
            print(stays)
            stays = stays.exclude(room__reservation__checkin_date__gt=check_out, room__reservation__checkout_date__lt=check_in)
           
            if self.checking_date(check_in,check_out) == True:
                stays = stays.annotate(price=Min('room__roomprice__cost__price'))

            if self.checking_date(check_in,check_out) == False:
                stays = stays.annotate(price=Max('room__roomprice__cost__price'))
            
            result = [{
                'id' : stay.id,
                'hotelNameKor' : stay.name,
                'price' : stay.price,
                'checkInDate' : stay.chek_in,
                'checkOutDate' : stay.chek_out,
                'baseNum' : stay.base_people,
                'maxNum' : stay.max_people,
                'category' : stay.category
            }for stay in stays]

            return JsonResponse({'result' : result}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEYERROR'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except FieldError:
            return JsonResponse({'message' : 'Bad_Request'}, status=404)