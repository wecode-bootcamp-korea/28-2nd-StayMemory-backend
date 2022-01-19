import jwt
import json
import zoneinfo

from datetime    import datetime
from django.test import TestCase, Client
from my_settings import SECRET_KEY, ALGORITHM

from reservations.models import Payment, Reservation, ReservationStatus
from stays.models        import Category, Cost, Room, RoomPrice, Stay
from users.models        import User
from admins.models       import Admin

class AdminPageTest(TestCase):
    def setUp(self):
        korea_tz = zoneinfo.ZoneInfo("Asia/Seoul")
        User.objects.create(
            id=1,
            kakao_id = 1,
            nickname = "제발되라",
            email = "cyl0504@naver.com",
            gender = 1,
        )
        Category.objects.create(
            id = 1,
            name = "호텔"
        )
        Admin.objects.create(
            id=2,
            name = "이찬영",
            admin_id = "admin",
            password = "123456",
            email = "cyl0504@naver.com"
        )
        Stay.objects.create(
            id              = 1,
            name            = "test호텔",
            expression      = "호텔설명입니다",
            description     = "한줄평입니다",
            city            = "강서구",
            state           = "서울",
            address         = "주소",
            thumbnail_url   = "img.url",
            description_url = "상세사진",
            launched_at     = "2012-01-26",
            category_id     = 1,
            admin_id        = 2,
        )
        Room.objects.create(
            id=1,
            stay_id=1,
            name="1호",
            room_description="조용한 방",
            check_in_time = "15:00",
            check_out_time = "11:00",
            base_num_people = 2,
            max_num_people = 4,
            area = 47,
            queen_bed = 1,
            single_bed = 1,
            double_bed = 1,
            policy = "금연방",
        )
        Cost.objects.create(
            id = 1,
            price = 56000,
            additional_price = 2000,
            cost_basis = 2,
        )
        Cost.objects.create(
            id = 2,
            price = 70000,
            additional_price = 2000,
            cost_basis = 2,
        )
        RoomPrice.objects.create(
            id = 1,
            room_id = 1,
            cost_id = 1,
        )
        RoomPrice.objects.create(
            id = 2,
            room_id = 1,
            cost_id = 2,
        )
        ReservationStatus.objects.create(
            id=1,
            status = "complete"
        )
        Payment.objects.create(
            id=1,
            name = "credit_card",
        )
        Reservation.objects.create(
            id = 1,
            user_id = 1,
            room_id = 1,
            reservation_status_id = 1,
            check_in_date = datetime(2022,1,2,23,59,59, tzinfo=korea_tz),
            check_out_date = datetime(2022,1,4,23,59,59, tzinfo=korea_tz),
            reservation_number = "d946fae5566b4218b27a612d3a77d0be",
            payment_id_id = 1,
            price = 56000,
            num_people = 2,
        )

        self.token = jwt.encode({"id":1}, SECRET_KEY, algorithm=ALGORITHM)

    def tearDown(self):
        Stay.objects.all().delete()
        Category.objects.all().delete()
        Admin.objects.all().delete()
        Payment.objects.all().delete()
        ReservationStatus.objects.all().delete()
        RoomPrice.objects.all().delete()
        Cost.objects.all().delete()
        Room.objects.all().delete()
        User.objects.all().delete()

    def test_reservation_information_view_get_success(self):
        client   = Client()
        headers  = {"HTTP_Authorization":self.token}
        response = client.get("/reservations?filter=reservation", **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data":[{
            "reservationId"    : 1,
            "reservationNumber": "d946fae5-566b-4218-b27a-612d3a77d0be",
            "hotelName"        : "test호텔",
            "hotelId"          : 1,
            "address"          : "서울 강서구 주소",
            "baseNum"          : 2,
            "maxNum"           : 4,
            "checkInDate"      : "2022-01-02",
            "checkOutDate"     : "2022-01-04",
            "price"            : 56000,
            "img"              : "img.url"
        }]})

    def test_reservation_information_view_get_400_error(self):
        client   = Client()
        headers  = {"HTTP_Authorization":self.token}
        response = client.get("/reservations?filters=reservation", **headers)
        self.assertEqual(response.status_code, 400)

    def test_reservation_information_view_post_success(self):
        client   = Client()
        headers  = {"HTTP_Authorization":self.token}
        bodys    = {
                "stayId": 1,
                "numPeople": 3,
                "checkin":  "2022-01-03",
                "checkout": "2022-01-05",
                "price": 55000,
                "payment": "credit_card",
        }
        response = client.post(
                "/reservations", 
                json.dumps(bodys),
                content_type = "application/json",
                **headers
        )
        self.assertEqual(response.status_code, 201)

    def test_reservation_information_view_post_400_error(self):
        client   = Client()
        headers  = {"HTTP_Authorization":self.token}
        bodys    = {
                "stayI": 1,
                "numPeople": 3,
                "checkin":  "2022-01-03",
                "checkout": "2022-01-05",
                "price": 55000,
                "payment": "credit_card",
        }
        response = client.post(
                "/reservations", 
                json.dumps(bodys),
                content_type = "application/json",
                **headers
        )
        self.assertEqual(response.status_code, 400)

    def test_reservation_information_view_post_400_error(self):
        client   = Client()
        headers  = {"HTTP_Authorization":self.token}
        bodys    = {
                "stayId": 2,
                "numPeople": 3,
                "checkin":  "2022-01-03",
                "checkout": "2022-01-05",
                "price": 55000,
                "payment": "credit_card",
        }
        response = client.post(
                "/reservations", 
                json.dumps(bodys),
                content_type = "application/json",
                **headers
        )
        self.assertEqual(response.status_code, 404)
