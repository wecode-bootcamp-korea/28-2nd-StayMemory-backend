import os
import csv
import django
import sys


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stay_memory.settings')
django.setup()

from users.models import User
from wishlists.models import Wishlist
from stays.models import Category, RoomImage, Stay, StayImage, Room, Cost, RoomPrice
from reservations. models import ReservationStatus, Payment, Reservation
from admins.models import Admin

#카테고리 첨부
Category.objects.get_or_create(name='호텔')
Category.objects.get_or_create(name='게스트하우스')

CSV_PATH_stays_Stay = './csv/stays_Stay.csv'

def stay():
    with open(CSV_PATH_stays_Stay) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        count = 1
        for row in data:
            if row[0]:
                name = row[0]
                expression = row[1]
                description = row[2]
                city = row[3]
                state = row[4]
                address = row[5]
                launched_at = row[6]
                category = row[7]
                admin_id = row[8]
                if(category == "게스트하우스"):
                    thumbnail_url=f"https://staymemory.s3.ap-northeast-2.amazonaws.com/guesthouses/guesthouses_{count}.jpg"
                else:
                    thumbnail_url=f"https://staymemory.s3.ap-northeast-2.amazonaws.com/hotels/hotels_{count-17}.jpg"

                description_url = thumbnail_url
                stay_category = Category.objects.get(name=category)
                Stay.objects.create(
                    name=name, 
                    expression=expression, 
                    description=description, 
                    city=city, 
                    state=state, 
                    address=address, 
                    thumbnail_url=thumbnail_url, 
                    description_url=description_url, 
                    launched_at=launched_at, 
                    category=stay_category, 
                )
                count+=1
# stay()

CSV_PATH_stays_Room = './csv/stays_Room.csv'

def room():
    with open(CSV_PATH_stays_Room) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                stay_id = row[0]
                name = row[1]
                room_description = row[2]
                check_in_time = row[3]
                check_out_time = row[4]
                base_num_people = row[5]
                max_num_people = row[6]
                area = row[7]
                queen_bed = row[8]
                single_bed = row[9]
                double_bed = row[10]
                policy = row[11]
                room_stay = Stay.objects.get(id=stay_id)
                Room.objects.create(
                    stay=room_stay,
                    name=name,
                    room_description=room_description,
                    check_in_time=check_in_time,
                    check_out_time=check_out_time,
                    base_num_people=base_num_people,
                    max_num_people=max_num_people,
                    area=area,
                    queen_bed=queen_bed,
                    single_bed=single_bed,
                    double_bed=double_bed,
                    policy=policy,
                )
# room()

CSV_PATH_stays_Cost = './csv/stays_Cost.csv'

def cost():
    with open(CSV_PATH_stays_Cost) as in_file:
        data = csv.reader(in_file)
        next(data,None)
        for row in data:
            if row[0]:
                price = row[0]
                additional_price = row[1]
                cost_basis = row[2]
                Cost.objects.create(price=price, additional_price=additional_price, cost_basis=cost_basis)
# cost()

CSV_PATH_stays_RoomPrice = './csv/stays_RoomPrice.csv'

def room_cost():
    with open(CSV_PATH_stays_RoomPrice) as in_file:
        data = csv.reader(in_file)
        next(data,None)
        for row in data:
            if row[0]:
                room_id = row[0]
                cost_id = row[1]
                room_info = Room.objects.get(id=room_id)
                cost_info = Cost.objects.get(id=cost_id)
                RoomPrice.objects.create(room=room_info, cost=cost_info)
# room_cost()