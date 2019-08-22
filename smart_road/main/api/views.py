from main.models import Pass,Camera,Road
from main.api.serializers import PassSerializer,CameraSerializer,RoadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
import geopy.distance
import sys

class GetCuLocation(APIView):

    def post(self,request,format = None):
        plate_char = request.POST["plate_char"]
        plate_num = request.POST["plate_num"]
        year = int(request.POST["year"])
        month = int(request.POST["month"])
        day = int(request.POST["day"])
        args = Pass.objects.filter(plate_char = plate_char,plate_num = plate_num)# or whatever arbitrary queryset
        max = 0
        l = None
        for i in args:
            if int(i.camera.sequence) > max and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                max = int(i.camera.sequence)
                l = i.camera

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
        year = int(request.POST["year"])
        month = int(request.POST["month"])
        day = int(request.POST["day"])

        args = Pass.objects.filter(plate_char = plate_char,plate_num = plate_num)# or whatever arbitrary queryset
        temp = list()
        for i in args:
            if int(i.hour) < hour and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                temp.append(i)
            elif int(i.hour) == hour and int(i.minute) <= minute and int(i.day) == day and int(i.year) == year and int(i.month) == month:
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
        year = int(request.POST["year"])
        month = int(request.POST["month"])
        day = int(request.POST["day"])
        tm = None
        p = Pass.objects.filter(camera_id=cam_id)
        temp = list()

        if m >= t:
            tm = m - t
            for i in p:
                if  int(i.hour) == h and int(i.minute) <= m and int(i.minute) >= tm and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                    temp.append(i)
        else:
            tm = 60 - (int(t) - int(m))
            for i in p:
                if  int(i.hour) == h  and int(i.minute) <= m and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                    temp.append(i)
                elif int(i.hour) == h - 1 and int(i.minute) >= tm and int(i.day) == day and int(i.year) == year and int(i.month) == month:
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
        year = int(request.POST["year"])
        month = int(request.POST["month"])
        day = int(request.POST["day"])
        args = Pass.objects.filter(plate_char = plate_char,plate_num = plate_num)
        max = 0
        min = sys.maxsize
        ma = None
        mi = None
        for i in args:
            if int(i.hour) < hour and int(i.camera.sequence) > max and int(i.hour) < hour and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                max = i.camera.sequence
                ma = i.camera
            elif  int(i.camera.sequence) > max and int(i.hour) == hour and int(i.minute) <= minute and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                max = i.camera.sequence
                ma = i.camera
            if int(i.hour) < hour and int(i.camera.sequence) < min and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                min = i.camera.sequence
                mi = i.camera
            elif  int(i.camera.sequence) < min and int(i.hour) == hour and int(i.minute) <= minute and int(i.day) == day and int(i.year) == year and int(i.month) == month:
                min = i.camera.sequence
                mi = i.camera
        if ma == None or mi == None:
            return Response("There are not any data!")\

        coords_1 = (ma.latitude,ma.longitude)
        coords_2 = (mi.latitude,mi.longitude)
        d =  geopy.distance.vincenty(coords_1, coords_2).km
        t = ma.hour - mi.hour
        if t == 0:
            t = 1
        elif d == 0:
            return Response("There are not enough data!")

        return Response(d/t)

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

class GetRoads(APIView):

    def get(self, request, format= None):
        r = Road.objects.all()
        serializer = RoadSerializer(r,many=True)
        return Response(serializer.data)

class GetCameras(APIView):
    def post(self, request, format= None):
        rid = request.POST["roadID"]
        r = Camera.objects.filter(road_id=rid)
        serializer = CameraSerializer(r,many=True)
        return Response(serializer.data)



        
