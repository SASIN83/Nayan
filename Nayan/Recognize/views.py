from django.shortcuts import render,redirect
from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import cv2
import time
from Project.Recognizer import FRDist
import pickle
import numpy as np
from PIL import Image
from Nayan.settings import BASE_DIR
import os
from Project.Register import ReportFileCreate, ReportFileEdit

MissingID,MissingEnck, MissingNames = pickle.load(open(os.path.join(BASE_DIR,'Project/MissingSet.pk'), 'rb'))
CriminalID,CriminalEnck, CriminalNames = pickle.load(open(os.path.join(BASE_DIR,'Project/CriminalSet.pk'), 'rb'))
enck,Names = MissingEnck + CriminalEnck, MissingNames + CriminalNames
MissingSetNames = set(MissingNames)
CriminalSetNames = set(CriminalNames)

def indexupload(request):
    if(request.method == 'POST'):
        if request.FILES.get('inputImage',None)!=None:
            inputImage=request.FILES['inputImage']
            img = Image.open(inputImage)
            col = cv2.cvtColor(np.array(img),cv2.COLOR_BGR2RGB)
            x = FRDist(col,enck,Names)
            try:
                if x!=None or x[0]!='Unknown':
                    return redirect('/app/upload/?success=True')
                else:
                    return redirect('/app/upload/?error=MFDorNF')
            
            except:
                return redirect('/app/upload/?error=NIS')
    else:
        return render(request,'recognize/upload.html')
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


