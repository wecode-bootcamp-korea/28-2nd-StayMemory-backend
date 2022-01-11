from django.test import TestCase, Client
from stays.views import StayListView

class JustTest(TestCase):
    def setUp(self):
        pass
    def test_success_checking_date_method(self):
        result =StayListView.checking_date("2022-2-11","2022-2-13")

        self.assertEqual(False,result)