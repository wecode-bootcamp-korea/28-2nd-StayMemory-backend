from django.test         import TestCase, Client
from reservations.models import Payment, Reservation, ReservationStatus
from stays.views         import StayListView
from stays.models        import Category, Cost, Room, RoomPrice, Stay
from users.models        import User
from admins.models       import Admin
class ListPageTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = 1,
            nickname = '제발되라',
            email    = 'cyl0504@naver.com',
            gender   = 1,
        )
        Category.objects.create(
            id   = 1,
            name = '호텔'
        )
        Admin.objects.create(
            id       =2,
            name     = '이찬영',
            admin_id = 'admin',
            password = '123456',
            email    = 'cyl0504@naver.com'
        )
        Stay.objects.create(
            id              = 1,
            name            = 'test호텔',
            expression      = '호텔설명입니다',
            description     = '한줄평입니다',
            city            = '강서구',
            state           = '서울',
            address         = '주소',
            thumbnail_url   = 'img.url',
            description_url = '상세사진',
            launched_at     = '2012-01-26',
            category_id     = 1,
            admin_id        = 2,
        )
        Room.objects.create(
            id               = 1,
            stay_id          = 1,
            name             = '1호',
            room_description = '조용한 방',
            check_in_time    = '15:00',
            check_out_time   = '11:00',
            base_num_people  = 2,
            max_num_people   = 4,
            area             = 47,
            queen_bed        = 1,
            single_bed       = 1,
            double_bed       = 1,
            policy           = '금연방',
        )
        Cost.objects.create(
            id               = 1,
            price            = 56000,
            additional_price = 2000,
            cost_basis       = 2,
        )
        Cost.objects.create(
            id               = 2,
            price            = 70000,
            additional_price = 2000,
            cost_basis       = 2,
        )
        RoomPrice.objects.create(
            id      = 1,
            room_id = 1,
            cost_id = 1,
        )
        ReservationStatus.objects.create(
            id     = 1,
            status = '예약중'
        )
        Payment.objects.create(
            id   = 1,
            name = '카드',
        )
        Reservation.objects.create(
            id                    = 1,
            user_id               = 1,
            room_id               = 1,
            reservation_status_id = 1,
            check_in_date         = '2022-1-3',
            check_out_date        = '2022-1-5',
            reservation_number    = 'd946fae5566b4218b27a612d3a77d0be',
            payment_id_id         = 1,
            price                 = 56000,
            num_people            = 2,
        )
        

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

    def test_key_error(self):
        client = Client()
        response = client.get('/stays/list',{'city':'서울', 'checkin':'2022-1-3', 'checkout':'2022-1-5', 'minprice':'56000', 'maxprice':'70000', 'category':'호텔', 'maxpeople':'4', 'sort':'price'})
        self.assertEqual(response.json(),{'data':[{
            'id'          : 1,
            'hotelNameKor': 'test호텔',
            'price'       : '56,000 ~ 56,000',
            'baseNum'     : 2,
            'maxNum'      : 4,
            'stayType'    : '호텔',
            'img'         : 'img.url',
        }]})