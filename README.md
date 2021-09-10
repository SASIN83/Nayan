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