from django.db import models


# Create your models here.


class Road(models.Model):
    road_id = models.CharField(primary_key=True,max_length=10)
    province = models.CharField(max_length = 20,blank = False,null = False)
    source = models.CharField(max_length = 20,blank = False,null = False)
    destination = models.CharField(max_length = 20,blank = False,null = False)

class Camera(models.Model):
    cam_id = models.CharField(primary_key=True,max_length=10,default = None)
    longitude = models.CharField(max_length = 10,blank = False,null = False,default = None)
    latitude = models.CharField(max_length = 10,blank = False,null = False,default = None)
    province = models.CharField(max_length = 20,blank = False,null = False,default = None)
    sequence = models.CharField(max_length = 5,blank = False,null = False,default = None)
    road = models.ForeignKey(Road, on_delete=models.CASCADE,default = None,blank = True,null = True)

class Pass(models.Model):
    pass_id = models.CharField(primary_key=True,max_length=10,default = None)
    plate_char = models.CharField(max_length=1,blank = False,null = False)
    plate_num = models.CharField(max_length=7,blank = False,null = False)
    speed = models.CharField(max_length = 3,blank = True,null = True)
    hour = models.IntegerField(blank = False,null = False)
    minute = models.IntegerField(blank = False,null = False)
    longitude = models.CharField(max_length = 10,blank = False,null = False,default = None)
    latitude = models.CharField(max_length = 10,blank = False,null = False,default = None)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE,default = None)
    road = models.ForeignKey(Road, on_delete=models.CASCADE,default = None)
