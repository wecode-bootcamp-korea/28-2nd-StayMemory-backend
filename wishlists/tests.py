import json
import requests

from django.test   import TestCase, Client
from unittest.mock import MagicMock, patch

from users.models    import User
from wishlists.models import Wishlist
from stays.models     import (Stay,
                              Room,
                              Cost,
                              RoomPrice)

class WishlistViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = "1234567",
            nickname = "kjy120924@gmail.com",
            gender   = 1,
        )
        Stay.objects.create(
            id              = 1,
            name            = "stays",
            expression      = "this is stays",
            description     = "test",
            city            = "강서구",
            state           = "서울특별시",
            address         = "201",
            thumbnail_url   = "http://test.com",
            description_url = "http://test.com",
            launched_at     = "2015-01-01",
            category        = None,
            admin           = None,
        )
        Stay.objects.create(
            id              = 3,
            name            = "stays",
            expression      = "this is stays",
            description     = "test",
            city            = "강서구",
            state           = "서울특별시",
            address         = "201",
            thumbnail_url   = "http://test.com",
            description_url = "http://test.com",
            launched_at     = "2015-01-01",
            category        = None,
            admin           = None,
        )
        Room.objects.create(
            id               = 1,
            stay_id          = 3,
            name             = "queen room",
            room_description = "This is good room!",
            check_in_time    = "12:00",
            check_out_time   = "10:00",
            base_num_people  = 3,
            max_num_people   = 4,
            area             = 47.12,
            queen_bed        = 1,
            single_bed       = 0,
            double_bed       = 0,
            policy           = "There is no policy!!",
        )
        Cost.objects.create(
            id=1,
            price = 70000,
            additional_price = 20000,
            cost_basis ="No!",
        )
        Cost.objects.create(
            id=2,
            price = 90000,
            additional_price = 20000,
            cost_basis ="No!",
        )
        RoomPrice.objects.create(
            id      = 1,
            room_id = 1,
            cost_id = 1,
        )
        RoomPrice.objects.create(
            id      = 2,
            room_id = 1,
            cost_id = 2,
        )
        Wishlist.objects.create(
            id      = 1,
            user_id = 1,
            stay_id = 3,
        )

    def tearDown(self):
        User.objects.all().delete()
        Stay.objects.all().delete()
        Room.objects.all().delete()
        Cost.objects.all().delete()
        Wishlist.objects.all().delete()

    def test_wishlist_view_post_create(self):
        client   = Client()
        token    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.AekHFMguragxj6mgkwhioYrEzr6tOktCW-vOYLj1P9M"
        bodys    = {"stayId":1}
        headers  = {"HTTP_Authorization":token}
        response = client.post(
            "/wishlists", 
            json.dumps(bodys),
            content_type='application/json',
            **headers,
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
                response.json(),
                {"message":"WISHLIST_IS_CREATED"}
        )

    def test_wishlist_view_post_delete(self):
        client   = Client()
        token    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.AekHFMguragxj6mgkwhioYrEzr6tOktCW-vOYLj1P9M"
        bodys    = {"stayId":3}
        headers  = {"HTTP_Authorization":token}
        response = client.post(
            "/wishlists", 
            json.dumps(bodys),
            content_type='application/json',
            **headers,
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message":"WISHLIST_IS_DELETED"}
        )
    def test_wishlist_view_post_404(self):
        client   = Client()
        token    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.AekHFMguragxj6mgkwhioYrEzr6tOktCW-vOYLj1P9M"
        bodys    = {"stayId":2}
        headers  = {"HTTP_Authorization":token}
        response = client.post(
            "/wishlists", 
            json.dumps(bodys),
            content_type='application/json',
            **headers,
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"message":"STAY_DOES_NOT_EXIST"},
        )

    def test_wishlist_view_get_success(self):
        client   = Client()
        token    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.AekHFMguragxj6mgkwhioYrEzr6tOktCW-vOYLj1P9M"
        headers  = {"HTTP_Authorization":token}
        response = client.get("/wishlists",**headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {"data":
                [
                    {
                        "id"          :1,
                        "hotelId"     :3,
                        "hotelNameKor":"stays",
                        "address"     :"서울특별시 강서구 201",
                        "baseNum"     :3,
                        "maxNum"      :4,
                        "price"       :"70,000 ~ 90,000",
                        "img"         :"http://test.com",
                    }
                ]
            }
        )
