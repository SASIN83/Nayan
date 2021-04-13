import numpy as np
import cv2
from Recognizer import FRDist
import pickle

MissingEnck, MissingNames = pickle.load(open('D:/PROJECTS/Django/Nayan/NayanEnvironment/Nayan/Project/MissingSet.pk', 'rb'))
CriminalEnck, CriminalNames = pickle.load(open('D:/PROJECTS/Django/Nayan/NayanEnvironment/Nayan/Project/CriminalSet.pk', 'rb'))
enck,Names = MissingEnck + CriminalEnck, MissingNames + CriminalNames
MissingSetNames = set(MissingNames)
CriminalSetNames = set(CriminalNames)
def videoset(enck,Names):
    cap = cv2.VideoCapture(0)
    
    namea = []
    while True: 
        rec, frame = cap.read()
        frame=cv2.flip(frame,1)
        x = FRDist(frame,enck,Names)
        if x!=None:
            print(x[0])
        namea.append(x)
        cv2.imshow('Nayan',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    names = list(dict.fromkeys(namea))
    z = 'Unknown'
    if names!=[]:
        x = [i for i in names if i != None]
        if 'Unknown' in x:
            x.remove('Unknown')
        if set(x) & set(CriminalNames):
            z = set(x) & set(CriminalNames)
            z = f'{",".join(z)} is/are Criminals'
            
        if set(x) & set(MissingNames):
            z = set(x) & set(MissingNames)
            z = f'{",".join(z)} is/are Missing'

    return z

def videosetter():
    return videoset(enck,Names)

