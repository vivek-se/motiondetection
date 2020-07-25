import cv2
from datetime import datetime
import numpy as np
from WebcamStreaming.models import camerastream


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.vcap = cv2.VideoCapture('http://192.168.43.1:8000/video')
        self.count=0
        self.total=0
        
    
    def __del__(self):
        self.video.release()

    
    def get_frame(self):
        #ip web cam
        suc, frame_ip = self.vcap.read()
        if frame_ip is not None:
            self.total=self.total+1
            if self.total%100 == 0:
                d_ip = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print('ip camera ', d_ip ,self.total)
                ip_object = camerastream.objects.create(timestamp = d_ip, camera_name = 'IP camera', frame_count = self.total)
                ip_object.save()
                
            
        # local web cam
        self.count=self.count+1
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        if self.count%100 == 0:
            d_loc = d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('local webcamera ', d_loc , self.count)
            loc_object = camerastream.objects.create(timestamp = d_loc, camera_name = 'Local webcamera', frame_count = self.count )
            loc_object.save()
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
      