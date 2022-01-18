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

class SignInKakaoView(View):
    def post(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            if access_token is None:
                 return JsonResponse({"message":"KAKAO_TOKEN_DOES_NOT_FOUND"}, status=401)

            profile = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization":f"Bearer {access_token}"}
            ).json()

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
