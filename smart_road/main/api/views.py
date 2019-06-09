from main.models import Pass,Camera,Road
from main.api.serializers import PassSerializer,CameraSerializer,RoadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max


class GetCuLocation(APIView):

    def post(self,request,format = None):
        plate_char = request.POST["plate_char"]
        plate_num = request.POST["plate_num"]
        args = Pass.objects.filter(plate_char = plate_char,plate_num = plate_num)# or whatever arbitrary queryset
        max = 0
        l = None
        for i in args:
            if int(i.camera.sequence) > max:
                max = i.camera.sequence
                l = i.camera
                break
        if l is not None:
            serializer = CameraSerializer(l)
            return Response(serializer.data)
        else :
            return Response("The car is not in bounds")

class GetLocations(APIView):

    def post(self,request,format = None):
        plate_char = request.POST["plate_char"]
        plate_num = request.POST["plate_num"]
        hour = int(request.POST["hour"])
        minute = int(request.POST["minute"])
        args = Pass.objects.filter(plate_char = plate_char,plate_num = plate_num)# or whatever arbitrary queryset
        temp = list()
        for i in args:
            if int(i.hour) < hour:
                temp.append(i)
            elif int(i.hour) == hour and int(i.minute) <= minute:
                temp.append(i)

        if len(temp) != 0:
            serializer = PassSerializer(temp,many=True)
            return Response(serializer.data)
        else :
            return Response("The car is not in bounds")

class GetNumCar(APIView):

    def post(self,request,format = None):
        seq = request.POST["sequence"]
        rid = request.POST["roadId"]
        cam_id = Camera.objects.filter(sequence=seq,road_id=rid).first().id
        h = int(request.POST["hour"])
        m = int(request.POST["minute"])
        t = int(request.POST["period"])
        tm = None
        p = Pass.objects.filter(camera_id=cam_id)
        temp = list()

        if m >= t:
            tm = m - t
            for i in p:
                if  int(i.hour) == h and int(i.minute) <= m and int(i.minute) >= tm:
                    temp.append(i)
        else:
            tm = 60 - (int(t) - int(m))
            for i in p:
                if  int(i.hour) == h  and int(i.minute) <= m:
                    temp.append(i)
                elif int(i.hour) == h - 1 and int(i.minute) >= tm:
                    temp.append(i)

        if len(temp) != 0:
            return Response(len(temp))
        else :
            return Response("The car is not in bounds")

class GetSpeedCar(APIView):

    def post(self,request,format = None):
        plate_char = request.POST["plate_char"]
        plate_num = request.POST["plate_num"]
        hour = int(request.POST["hour"])
        minute = int(request.POST["minute"])
        args = Pass.objects.filter(plate_char = plate_char,plate_num = plate_num)# or whatever arbitrary queryset
        total = 0
        num = 0
        for i in args:
            if int(i.hour) < hour:
                num = num + 1
                total = total + int(i.speed)
            elif int(i.hour) == hour and int(i.minute) <= minute:
                num = num + 1
                total = total + int(i.speed)
        if num != 0:
            return Response(total/num)
        else:
            return Response("There are not any data!")



class CreateCamera(APIView):
    def post(self, request, format= None):
        serializer = CameraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cid = request.POST["cam_id"]
            rid = request.POST["roadID"]
            c = Camera.objects.filter(cam_id = cid).first()
            c.road = Road.objects.filter(road_id = rid).first()
            c.save()
            return Response("The camera is registered successfully!", status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)

class UpdateCamera(APIView):
    def post(self, request, format= None):
        cid = request.POST["cam_id"]
        rid = request.POST["roadID"]
        la = request.POST["latitude"]
        lo = request.POST["longitude"]
        pr = request.POST["province"]
        seq = request.POST["sequence"]
        c = Camera.objects.filter(cam_id = cid).first()
        c.road = Road.objects.filter(road_id = rid).first()
        c.longitude = lo
        c.latitude = la
        c.province = pr
        c.sequence = seq
        c.save()
        return Response("The camera is updated successfully!", status=status.HTTP_200_OK)

class CreateRoad(APIView):
    def post(self, request, format= None):
        serializer = RoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("The road is registered successfully!", status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)
