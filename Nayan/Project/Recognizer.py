import cv2
import pickle
import face_recognition
#from .Train import byte2image, image2byte
import numpy as np
import os
from Nayan.settings import BASE_DIR
from .Register import ReportFileCreate, ReportFileEdit 



MissingID,MissingEnck, MissingNames = pickle.load(open(os.path.join(BASE_DIR,'Project/MissingSet.pk'), 'rb'))
CriminalID,CriminalEnck, CriminalNames = pickle.load(open(os.path.join(BASE_DIR,'Project/CriminalSet.pk'), 'rb'))
IDS,enck,Names = MissingID+CriminalID, MissingEnck + CriminalEnck, MissingNames + CriminalNames
MissingSetNames = set(MissingNames)
CriminalSetNames = set(CriminalNames)
namea=[]

def FRDist(frame,enck,Names):
    faceFrame= face_recognition.face_locations(frame)
    encFrame= face_recognition.face_encodings(frame,faceFrame)
    for encodeFace,faceloc in zip(encFrame,faceFrame):
        match = face_recognition.compare_faces(enck,encodeFace)
        faceDis= face_recognition.face_distance(enck,encodeFace)
        matchindex=np.argmin(faceDis)
        name = 'Unknown'
        category = 'Green'
        if match[matchindex] and faceDis[matchindex]<=0.49:
            name=Names[matchindex].upper()
            y1,x2,y2,x1=faceloc
            ids=''
            if name in CriminalNames:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.putText(frame,name,(x1+6,y1-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.imwrite(os.path.join(BASE_DIR,'/Recognize/recognized/Criminal/'+f'{name}.jpg'),frame)
                category = 'Criminal/Red'
                ids=IDS[matchindex]
                if ids not in namea:
                    namea.append(ids)
                    ReportFileEdit(name,category,ids)
            if name in MissingNames:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,255),2)
                cv2.putText(frame,name,(x1+6,y1-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
                cv2.imwrite(os.path.join(BASE_DIR,'/Recognize/recognized/Missing/'+f'{name}.jpg'),frame)
                category = 'Missing/Yellow'
                ids=IDS[matchindex]
                if ids not in namea:
                    namea.append(ids)
                    ReportFileEdit(name,category,ids)
        else:
            name='Unknown'
            y1,x2,y2,x1=faceloc
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,name,(x1+6,y1-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        
        return [name,category]
