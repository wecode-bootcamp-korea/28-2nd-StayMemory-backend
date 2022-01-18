from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Max, Min, Q
from django.core.exceptions import FieldError
from datetime               import datetime, timedelta

from stays.models        import Stay, Room
from reservations.models import Reservation
from utils.convert_price import convert_price
from utils.check_weekday import include_weekday_boolean

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

class DetailPageView(View):
    def get(self, rquest, *args, **kwargs):
        try:
            stay_id = kwargs["stay_id"]

            stay = Stay.objects.get(id=stay_id)
            room = stay.room_set.first()
            data = {
                "hotelId"         : stay.id,
                "hotelName"       : stay.name,
                "hotelDescription": stay.expression,
                "checkin"         : room.check_in_time,
                "checkout"        : room.check_out_time,
                "headCount"       : room.base_num_people,
                "img"             : stay.thumbnail_url,
                "area"            : room.area
                "bed":{
                    "queen_bed" :room.queen_bed,
                    "single_bed":room.single_bed,
                    "double_bed":room.double_bed,
                },
            }
            return JsonResponse({"data":data}, status=200)

        except Stay.DoesNotExist:
            return JsonResponse({"message":"STAY_DOES_NOT_EXIST"}, status=404)

class UnavailableDateView(View):
    def get(self, request, *args, **kwargs):
        try:
            start_date = request.GET["start-date"]
            stay_id    = kwargs["stay_id"]
          
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date   = start_date + timedelta(days=186)

            room = Room.objects.get(stay_id = stay_id)
            reservations = Reservation.objects.filter(
                room                = room,
                check_in_date__lte  = end_date,
                check_out_date__gte = start_date,
            )

            unavailable_date = []
            for reservation in reservations:
                checkin_date  = reservation.check_in_date
                checkout_date = reservation.check_out_date
                days = (checkout_date-checkin_date).days
                unavailable_date += [
                    (checkin_date+timedelta(days=i)).strftime("%Y-%m-%d") 
                    for i in range(days)
                ]
                
            data = {"date":unavailable_date}
            return JsonResponse({"data":data}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except Room.DoesNotExist:
            return JsonResponse({"message":"ROOM_DOES_NOT_EXIST"}, status=404)

class CalcPriceView(View):
    def calc_price(self, additional_num_people, 
                   weekday_price, weekend_price, additional_price,
                   start_date, end_date):

        start_date  = datetime.strptime(start_date, "%Y-%m-%d")
        end_date    = datetime.strptime(end_date, "%Y-%m-%d")
        days        = (end_date-start_date).days
        price       = [weekday_price, weekday_price, weekday_price, weekday_price,
                       weekend_price, weekend_price, weekend_price]
        price_list = [
            price[(start_date+timedelta(days=i)).weekday()] 
            for i in range(days)
        ]
        total_price = sum(price_list) + days*additional_num_people*additional_price
        return total_price

    def get(self, request, *args, **kwargs):
        try:
            start_date = request.GET["start-date"]
            end_date   = request.GET["end-date"]
            num_people = int(request.GET["num-people"])
            stay_id    = kwargs["stay_id"]
            room       = Room.objects.filter(stay_id = stay_id)

            if not room:
                return JsonResponse({"message":"ROOM_DOES_NOT_EXIST"}, status=404)

            room_price = room.aggregate(weekend_price = Max("roomprice__cost__price"),
                                        weekday_price = Min("roomprice__cost__price"))

            weekday_price         = room_price['weekday_price']
            weekend_price         = room_price['weekend_price']
            base_num_people       = room.first().base_num_people
            additional_price      = room.first().roomprice_set.first().cost.additional_price
            additional_num_people = num_people - base_num_people 

            if additional_num_people < 0:
                additional_num_people = 0

            total_price = self.calc_price(
                additional_num_people,
                weekday_price, 
                weekend_price, 
                additional_price,
                start_date, 
                end_date
            )

            data = {"total_price": convert_price(total_price)}
            return JsonResponse({"data":data},status=200)
             
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
