from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from Recognize.models import ImageUploader
from Recognize.forms import ImageForm, FilterForm
from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError, JsonResponse
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
from django.views.generic import TemplateView
import io
from django.views.decorators.csrf import csrf_exempt
import base64
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
            
            if x!=None or x[0]!='Unknown':
                return redirect('/app/upload/?success=True')
            else:
                return redirect('/app/upload/?error=MFDorNF')
            
        else:
                return redirect('/app/upload/?error=NIS')
        
    else:
        return render(request,'recognize/upload.html')


def base64_decode(data):
    # with open('sample.png', 'wb') as f:
    #     f.write(base64.decodestring(data.split(',')[1].encode()))
    out=base64.decodestring(data.split(',')[1].encode())
    return out
     

def base64_encode(data):
    if data:
        return 'data:image/png;base64,' + data

class ImageFaceDetect(TemplateView):
    template_name = 'recognize/image.html'

    def post(self, request, *args, **kwargs):
        data = request.POST.get('image')
        try:
            base = base64_decode(data)
            nparr = np.fromstring(base, np.uint8)
            imgd = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            data = cv2.cvtColor(np.array(nparr),cv2.COLOR_BGR2RGB)
            image_data = FRDist(imgd,enck,Names)
            #image=cv2.imencode('.jpg',img)[1]
            buffer = io.BytesIO()
            img = Image.fromarray(data)
            img.save(image_data[0], format="png")
            encoded_string = base64.b64encode(buffer.getvalue()).decode('ascii')
            if image_data:
                if image_data!='Unknown':
                    if image_data[1] == "Missing/Yellow":
                        with open("Missing/"+image_data[0]+'.png','wb') as f:
                            f.write(base)
                    if image_data[1] == "Missing/Yellow":
                        with open("Criminal/"+image_data[0]+'.png','wb') as f:
                            f.write(base)
                return JsonResponse(status=200, data={'image': encoded_string, 'message': str(image_data[0])+', '+str(image_data[1])})
        except Exception as e:
            print(e)
        return JsonResponse(status=400, data={'errors': {'error_message': 'No face detected'}})


def indexscreen(request): 
    template = "recognize/screens.html"
    return render(request,template)
    
def index(request): 
    template = "recognize/index.html"
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

@csrf_exempt
def gallary(request):
    imgform = ImageForm()
    filterform = FilterForm()
    img=[]
    if request.method == 'POST':
        imgform = ImageForm(request.POST, request.FILES)
        filterform = FilterForm(request.POST)
        img = ImageUploader.objects.all()
        if imgform.is_valid():
            imgform.save()
            imgform = ImageForm()
            return render(request, 'recognize/gallary.html', {'imgform': imgform, 'filterform': filterform, 'img': img})
        if filterform.is_valid():
            if str(request.POST['filter']) == 'all':
                img = ImageUploader.objects.all()
            else:
                img = ImageUploader.objects.filter(category=str(request.POST['filter']))
            filterform = FilterForm()
            imgform = ImageForm()
            return render(request, 'recognize/gallary.html', {'imgform': imgform,'filterform': filterform, 'img': img})
    try:
        if request.method == 'GET':
            img = ImageUploader.objects.filter(category='miss')
        return render(request, 'recognize/gallary.html', {'imgform': imgform,'filterform': filterform, 'img': img})
    except:
        return render(request, 'recognize/gallary.html', {'imgform': imgform,'filterform': filterform})


def success(request):
    return HttpResponse('successfully uploaded')