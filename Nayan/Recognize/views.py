from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import cv2
import time
from Project.Recognizer import FRDist
import pickle
import numpy as np
from Nayan.settings import BASE_DIR
import os
from Project.Register import ReportFileCreate, ReportFileEdit

MissingID,MissingEnck, MissingNames = pickle.load(open(os.path.join(BASE_DIR,'Project/MissingSet.pk'), 'rb'))
CriminalID,CriminalEnck, CriminalNames = pickle.load(open(os.path.join(BASE_DIR,'Project/CriminalSet.pk'), 'rb'))
enck,Names = MissingEnck + CriminalEnck, MissingNames + CriminalNames
MissingSetNames = set(MissingNames)
CriminalSetNames = set(CriminalNames)


def indexscreen(request): 
    template = "recognize/screens.html"
    return render(request,template)
    
def index(request): 
    template = "recognize/home.html"
    return render(request,template)

def get_frame():
    cap =cv2.VideoCapture(0+cv2.CAP_DSHOW)
    while True:
        _, frame = cap.read()
        frame=cv2.flip(frame,1)
        x = FRDist(frame,enck,Names)
        imgencode = cv2.imencode('.jpg',frame)[1]
        stringData= imgencode.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+ stringData +b'\r\n')

    cap.release()
    cv2.destroyallwindows()

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")

    except :
        return "error"


