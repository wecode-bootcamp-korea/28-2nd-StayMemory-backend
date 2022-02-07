import json
import uuid
import boto3

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from stays.models  import Stay
from admins.models import Admin
from my_settings   import (AWS_ACCESS_KEY,
                           AWS_SECRET_KEY,
                           S3_BUCKET_NAME)

class AwsS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
             aws_access_key_id     = access_key,
             aws_secret_access_key = secret_key,
        )

        self.s3_client   = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, directory, file_obj):
        try:
            file_id    = str(uuid.uuid4())
            extra_args = {'ContentType': file_obj.content_type}
            filename   = f"{directory}/{file_id}.jpg" 

            self.s3_client.put_object(
                Key    = filename,
                Body   = file_obj,
                Bucket = self.bucket_name,
            )

            return f"https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{filename}"

        except:
            return None

class AdminStayView(View):
    def get(self, request, *args, **kwargs):
        try:
            admin_id = kwargs["admin_id"]
            offset   = request.GET.get("offset",0)
            limit    = request.GET.get("limit",10)

            admin    = Admin.objects.get(id=admin_id)
            stays    = Stay.objects.filter(admin=admin)
            data =[
                {
                    "hotelId"  : stay.id,
                    "hotelType": stay.category.name,
                    "address"  : f"{stay.state} {stay.city} {stay.address}",
                    "baseNum"  : stay.room_set.first().base_num_people,
                    "maxNum"   : stay.room_set.first().max_num_people,
                    "img"      : stay.thumbnail_url,
                    "price"    : stay.room_set.first()\
                                .roomprice_set.order_by("-cost__price")[0]\
                                .cost.price,
                }for stay in stays[offset:offset+limit]
            ]

            return JsonResponse({"data":data}, status=200)

        except Admin.DoesNotExist:
            return JsonResponse({"message":"ADMIN_DOES_NOT_EXIST"}, status=404)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            stay_id  = request.GET["stay-id"]
            admin_id = kwargs["admin_id"]
            image      = request.FILES.get('img', None)
            hotel_name = request.POST.get('name', None)
            price      = request.POST.get('price', None)
           
            stay = Stay.objects.get(id=stay_id)
            if not image and not hotel_name and not price:
                return JsonResponse({"message":"NO_VALUE"}, status=400)
            
            if image:
                aws_s3_client = AwsS3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME)
                image_url     = aws_s3_client.upload("stays", image)
                if not image_url:
                    return JsonResponse({"message":"S3_UPLOAD_ERROR"}, status=400)

                stay.thumbnail_url=image_url
                stay.save()

            if hotel_name:
                stay.name = hotel_name
                stay.save()

            if price:
                cost = stay.room_set.first()\
                      .roomprice_set.order_by("-cost__price")[0].cost
                cost.price = price
                cost.save()
            return JsonResponse({"message":"success"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except Stay.DoesNotExist:
            return JsonResponse({"message":"STAY_DOES_NOT_EXIST"}, status=404)

        except Admin.DoesNotExist:
            return JsonResponse({"message":"ADMIN_DOES_NOT_EXIST"}, status=404)

    def delete(self, request, *args, **kwargs):
        try:
            admin_id = kwargs["admin_id"]
            stay_id  = request.GET["stay-id"]
            admin    = Admin.objects.get(id=admin_id)
            stay     = Stay.objects.get(admin=admin, id=stay_id)

            stay.admin = None
            stay.save()

            return JsonResponse({"message":"STAY_IS_DELETED"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except Stay.DoesNotExist:
            return JsonResponse({"message":"STAY_DOES_NOT_EXIST"}, status=404)

        except Admin.DoesNotExist:
            return JsonResponse({"message":"ADMIN_DOES_NOT_EXIST"}, status=404)
