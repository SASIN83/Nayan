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
<<<<<<< Updated upstream
            col = cv2.cvtColor(np.array(img),cv2.COLOR_BGR2RGB)
            x = FRDist(col,enck,Names)
            
            if x!=None or x[0]!='Unknown':
                return redirect('/app/upload/?success=True')
=======
            #col = cv2.cvtColor(np.array(img),cv2.COLOR_BGR2RGB)
            col = np.array(img)
            image_data_result = FRDist(col,enck,Names)

            if image_data_result and image_data_result[0] != 'Unknown':
                name = image_data_result[0]
                category = image_data_result[1]
                coords = image_data_result[2]

                    # 5. Saving Logic (SAFE VERSION)
                    # If you want to save the image with boxes drawn by FRDist:
                    
                    # Convert back to BGR so colors look right when saved
                    # output_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                    
                    # Define a safe path (Ensure 'media/detections' exists)
                    # filename = f"detection_{name}_{np.random.randint(1000)}.jpg"
                    # save_path = os.path.join(settings.MEDIA_ROOT, 'detections', filename)
                    # cv2.imwrite(save_path, output_img)

                return JsonResponse({
                        'message': 'Success',
                        'name': name,
                        'category': category,
                        'coords': coords
                    })    
>>>>>>> Stashed changes
            else:
                return JsonResponse({'errors': {'error_message': 'No face detected or not in database'}})
            
        else:
            return JsonResponse({'errors': {'error_message': 'No Image Selected'}})
        
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
            image_data = FRDist(imgd,enck,Names)
            if image_data and image_data[0] != 'Unknown':
                name = image_data[0]
                category = image_data[1]
                # Save logic
                if category == "Missing/Yellow":
                    with open("Missing/"+name+'.png','wb') as f:
                        f.write(base)
                elif category == "Criminal/Red":
                    with open("Criminal/"+name+'.png','wb') as f:
                        f.write(base)
                return JsonResponse({
                    'message': 'Success',
                    'name': name,
                    'category': category
                })
            else:
                return JsonResponse({'errors': {'error_message': 'No face detected or not in database'}})
        except Exception as e:
            print(e)
            return JsonResponse({'errors': {'error_message': 'Error processing image'}})


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


<<<<<<< Updated upstream
=======
@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            if image_data:
                # 1. Robust Base64 Decoding (Prevents IndexError)
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                
                try:
                    
                    base = base64.b64decode(image_data)
                    nparr = np.frombuffer(base, np.uint8)
                    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if img_bgr is None or img_bgr.size == 0:
                        pass
                    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                    # Calculate average brightness (0 = Black, 255 = White)
                    avg_brightness = np.mean(gray)

                    if avg_brightness < 10:  # Threshold for "Too Dark/Black"
                        return JsonResponse({'errors': {'error_message': 'Image too dark / Camera covered'}})
                except Exception:
                    return JsonResponse({'errors': {'error_message': 'Invalid Image Data'}})

                # 2. CRITICAL FIX: Resize to prevent RAM Crash
                # Keeps image small enough for fast processing, big enough for recognition
                height, width = img_bgr.shape[:2]
                if width == 0 or height == 0:
                    return JsonResponse({'errors': {'error_message': 'Invalid image dimensions'}})
                # More aggressive resizing to reduce memory usage
                max_width = 480  # Reduced from 800 to 480 for lower memory
                if width > max_width:
                    scaling_factor = max_width / float(width)
                    img_bgr = cv2.resize(img_bgr, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

                # 3. Convert to RGB for Recognition
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                # 4. Process Recognition
                # This blocks the server until finished. Since you resized the image,
                # this should now take 0.2s - 0.5s instead of 5s+.
                image_data_result = FRDistVideo(img_rgb, enck, Names)

                if image_data_result and image_data_result[0] != 'Unknown':
                    name = image_data_result[0]
                    category = image_data_result[1]
                    coords = image_data_result[2]

                    # 5. Saving Logic (SAFE VERSION)
                    # If you want to save the image with boxes drawn by FRDist:
                    
                    # Convert back to BGR so colors look right when saved
                    # output_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                    
                    # Define a safe path (Ensure 'media/detections' exists)
                    # filename = f"detection_{name}_{np.random.randint(1000)}.jpg"
                    # save_path = os.path.join(settings.MEDIA_ROOT, 'detections', filename)
                    # cv2.imwrite(save_path, output_img)

                    return JsonResponse({
                        'message': 'Success',
                        'name': name,
                        'category': category,
                        'coords': coords
                    })
                else:
                    return JsonResponse({'errors': {'error_message': 'No face detected or not in database'}})
            
        except Exception as e:
            # Print the actual error to your console so you can debug
            print(f"Error processing image: {str(e)}")
            return JsonResponse({'errors': {'error_message': 'Error processing image'}})

    return JsonResponse({'errors': {'error_message': 'Invalid request'}})
# def process_image(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)
#         image_data = data.get('image')

#         if image_data:
#             try:
#                 # Decode base64 image
#                 base = base64_decode(image_data)
#                 nparr = np.frombuffer(base, np.uint8)
#                 imgd = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#                 # Process the image for face recognition
#                 image_data_result = FRDist(imgd, enck, Names)

#                 if image_data_result and image_data_result[0] != 'Unknown':
#                     # Save recognized image if needed
#                     if image_data_result[1] == "Missing/Yellow":
#                         os.makedirs(os.path.join(BASE_DIR, 'Recognize/recognized/Missing'), exist_ok=True)
#                         cv2.imwrite(os.path.join(BASE_DIR, 'Recognize/recognized/Missing', f'{image_data_result[0]}.png'), imgd)
#                     elif image_data_result[1] == "Criminal/Red":
#                         os.makedirs(os.path.join(BASE_DIR, 'Recognize/recognized/Criminal'), exist_ok=True)
#                         cv2.imwrite(os.path.join(BASE_DIR, 'Recognize/recognized/Criminal', f'{image_data_result[0]}.png'), imgd)

#                     return JsonResponse({'message': f'Recognized: {image_data_result[0]}, {image_data_result[1]}'})
#                 else:
#                     return JsonResponse({'errors': {'error_message': 'No face detected or not in database'}})
#             except Exception as e:
#                 print(f"Error processing image: {e}")
#                 return JsonResponse({'errors': {'error_message': 'Error processing image'}})

#     return JsonResponse({'errors': {'error_message': 'Invalid request'}})


>>>>>>> Stashed changes
def success(request):
    return HttpResponse('successfully uploaded')