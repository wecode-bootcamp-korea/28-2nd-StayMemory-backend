import jwt
import datetime
import requests
from django.views import View
from django.http  import JsonResponse

from my_settings  import (KAKAO_KEY,
                          KAKAO_SECRET,
                          SECRET_KEY,
                          ALGORITHM)

from users.models         import User
from utils.gender         import Gender
from utils.login_required import login_required
from reservations.models  import Reservation

class KakaoClient:
    def __init__(self, kakao_token):
        self.token  = kakao_token
        self.url    = "https://kapi.kakao.com/v2/user/me"
        self.header = {"Authorization":f"Bearer {kakao_token}"}

    def get_user_information(self):
        return requests.get(self.url, headers=self.header).json()

class SignInKakaoView(View):
    def post(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            if access_token is None:
                 return JsonResponse({"message":"KAKAO_TOKEN_DOES_NOT_FOUND"}, status=401)

            kakao_client = KakaoClient(access_token)
            profile      = kakao_client.get_user_information()

            kakao_id = profile.get("id", None)

            if kakao_id is None:
                return JsonResponse({"message":"KAKAO_TOKEN_ERROR"}, status=403)

            kakao_properties = profile.get("properties")
            kakao_account    = profile.get("kakao_account")
            nickname         = kakao_properties["nickname"]
            email            = kakao_account.get("email", None)
            gender           = kakao_account.get("gender", "unknown_")

            user, is_created = User.objects.update_or_create(
                kakao_id = kakao_id,
                defaults = {
                    "nickname" : nickname,
                    "email"    : email,
                    "gender"   : Gender[gender].value,
                }
            )

            message = "SUCCESS"
            status  = 200

            if is_created:
                message = "USER_CREATED"
                status  = 201

            exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            my_token = jwt.encode(
                {"id":user.id, "exp":exp_time},
                SECRET_KEY,
                algorithm=ALGORITHM
            )

            data = {
                "message" : message,
                "token"   : my_token,
            }
        
            return JsonResponse(data, status=status)

        except KeyError as e:
            return JsonResponse({"message":getattr(e,"message",str(e))},status=400)


class UserInformationView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            data = {
                "nickname"    : user.nickname,
                "email"       : user.email,
                "gender"      : Gender(user.gender).name,
                "travelNumber": Reservation.objects.filter(user=user).count()
            }
            return JsonResponse({"data":data}, status=200)

        except KeyError as e:
            return JsonResponse({"message":getattr(e,"message",str(e))},status=400)

        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"},status=404)
