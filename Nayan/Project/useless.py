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

MissingEnck, MissingNames = pickle.load(open(os.path.join(BASE_DIR,'Project/MissingSet.pk'), 'rb'))
CriminalEnck, CriminalNames = pickle.load(open(os.path.join(BASE_DIR,'Project/CriminalSet.pk'), 'rb'))
enck,Names = MissingEnck + CriminalEnck, MissingNames + CriminalNames
MissingSetNames = set(MissingNames)
CriminalSetNames = set(CriminalNames)

def get_frame():
    cap =cv2.VideoCapture(0)
    namea = []
    while True:
        _, frame = cap.read()
        frame=cv2.flip(frame,1)
        x = FRDist(frame,enck,Names)
        imgencode = cv2.imencode('.jpg',frame)[1]
        stringData= imgencode.tostring()
        if x!=None and x[0]!='Unknown':
            print(x[0])
            namea.append(x[0])

        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+ stringData +b'\r\n')
    cap.release()
    del(cap)
    
    
def indexscreen(request): 
    try:
        template = "screens.html"
        return render(request,template)
    except HttpResponseServerError:
        print("error")

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"