# NAYAN: VIRTUAL POLICE STATION
##### DJANGO BASED SYSTEM WITH FACE RECOGNITION USING FACE_RECOGNITION_API

  * This face recognition based virtual police station. 
  * Currently this supports only single face based input, with google docs as a form of FIR and a boring image gallery with only image and name of persons.
  * Training new image and adding it to database is still done manually. 
  * Everything related to backend is in Project repository and everything related to Django is in Recognizer directory. 
  * This uses IP geolocation of device to register any recognized faces and writes it to a csv file with its date in the filename automatically using pandas in Project/register.py. 
  * Training is done in Project/Train.py. 
  * Recognition is done by Project/Recognize.py. 
  * Chatbot feature is still not yet developed so any independent contribution is welcomed.

## Nayan Demo on Youtube

[![IMAGE ALT TEXT HERE](https://i.ytimg.com/vi/czHbuRs_dys/hqdefault.jpg)](https://youtu.be/czHbuRs_dys)

Note: 
  * If you can't install dlib for whatever reason, then just clone https://github.com/SASIN83/dlibpreinstalled and use pip install on file given in the repo. 
  * Also use of python 3.7.9 is recommended as dlib is most stable for this version of python.
