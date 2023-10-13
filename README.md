# NAYAN: VIRTUAL POLICE STATION
##### DJANGO BASED FACE RECOGNITION SYSTEM USING FACE_RECOGNITION_API

  * This face recognition based virtual police station. 
  * Currently this supports only single face based input, with google docs as a form of FIR and a boring image gallery with only image and name of persons.
  * Training new image and adding it to database is still done manually. 
  * Everything related to backend is in Project repository and everything related to Django is in Recognizer directory. 
  * This uses IP geolocation of device to register any recognized faces and writes it to a csv file with its date in the filename automatically using pandas in Project/register.py. 
  * Training is done in Project/Train.py. (Note: Training will only work when the name of image is in this format "ID.Name.jpeg", sometimes the image name is "ID Name.jpeg" which does not work as Train.py splits id,name,extension using "." as a seperator to save it in encoding as label.)
  * Delete old pickle(.pkl) files before training or modify Train.py to append new faces in the file.
  * Recognition is done by Project/Recognize.py. 
  * Chatbot feature is still not yet developed so any independent contribution is welcomed.

## Nayan Demo on Youtube

[![IMAGE ALT TEXT HERE](https://i.ytimg.com/vi/czHbuRs_dys/hqdefault.jpg)](https://youtu.be/czHbuRs_dys)

## Setup
```
pip install -r requirements.txt
```
```
cd Nayan
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py runserver
```

Note: 
  * If you can't install and build dlib for whatever reason, then just clone/download https://github.com/SASIN83/dlibpreinstalled and run
```
pip install dlib-19.19.0-cp37-cp37m-win_amd64.whl
```

  * Also use of python 3.7.9 is recommended as dlib is most stable for this version of python and I have used it in this project.
