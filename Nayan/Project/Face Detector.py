import cv2
import os
import face_recognition
import numpy as np

path = 'D:/PROJECTS/Django/Nayan/NayanEnvironment/Nayan/Project/'
cascades = 'D:/PROJECTS/Django/Nayan/NayanEnvironment/Lib/site-packages/cv2/data/'
def Detector():
    ori_img = cv2.imread(f'{path}images/BharaIMC.jpeg')
    col_image = cv2.cvtColor(ori_img,cv2.COLOR_BGR2BGRA)
    face_cascade = cv2.CascadeClassifier(f'{cascades}haarcascade_frontalface_alt2.xml')
    detected_faces = face_cascade.detectMultiScale(col_image,scaleFactor=1.115,minNeighbors=5,flags = cv2.CASCADE_SCALE_IMAGE)

    c = 0
    for (column, row, width, height) in detected_faces:
        x,y,w,h = column, row, width, height
        r = cv2.rectangle(
            ori_img,
            (column, row),
            (column + width, row + height),
            (0, 255, 0),
            2
        )
        r
        c+=1
        corimg= col_image[y:y+h,x:x+w]
        cv2.imwrite(os.path.join(f'{path}detected',f'img{c}.jpg'),corimg)
    source = f'{path}/images/sarthak.jpeg'
    cv2.imshow('Source',cv2.imread(source))
    cv2.imshow('Image', ori_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    known = face_recognition.load_image_file(f'{source}')
    known_encoding = face_recognition.face_encodings(known)[0]
    result = []
    for (root,dirs,files) in os.walk(f'{path}detected', topdown=True):
        print(files)
        for i in range(len(files)):
            unknown = face_recognition.load_image_file(f'{path}detected/{files[i]}')
            en=face_recognition.face_encodings(unknown)
            unknown_encoding = ''
            if len(en)!=0:
                unknown_encoding = en[0]
            
                results = face_recognition.compare_faces([known_encoding], unknown_encoding)
                if results!=[False]:
                    result.append("True")
                else:
                    result.append("False")
        
    
    if "True" in result:
        return "Person in source identified"
    else:
        return "Person in source not identified"
            

print(Detector())