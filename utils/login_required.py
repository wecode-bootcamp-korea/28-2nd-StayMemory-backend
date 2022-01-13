import jwt

from django.http import JsonResponse

from users.models import User
from my_settings  import (SECRET_KEY,
                          ALGORITHM)

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload.get('id'))
            request.user = user

            return func(self, request, *args, **kwargs)


        except KeyError as e:
            return JsonResponse({'message':getattr(e,'message',str(e))}, status=401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':"INVALID_TOKEN"}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'TOKEN_Expired'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'UserDoesNotExist'}, status=400)

    return wrapper
