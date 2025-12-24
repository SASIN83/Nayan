import cv2
import pickle
from deepface import DeepFace
import numpy as np
import os
from .save_detection_once import save_detection_once
from Nayan.settings import BASE_DIR
from .Register import ReportFileCreate, ReportFileEdit



MissingID,MissingEnck, MissingNames = pickle.load(open(os.path.join(BASE_DIR,'Project/MissingSet.pk'), 'rb'))
CriminalID,CriminalEnck, CriminalNames = pickle.load(open(os.path.join(BASE_DIR,'Project/CriminalSet.pk'), 'rb'))
IDS,enck,Names = MissingID+CriminalID, MissingEnck + CriminalEnck, MissingNames + CriminalNames
MissingSetNames = set(MissingNames)
CriminalSetNames = set(CriminalNames)
namea=[]

# def FRDist(frame,enck,Names):
#     try:
#         faces = DeepFace.extract_faces(img_path=frame, detector_backend='opencv', enforce_detection=False)
#         for face_data in faces:
#             facial_area = face_data['facial_area']
#             x = facial_area['x']
#             y = facial_area['y']
#             w = facial_area['w']
#             h = facial_area['h']
#             x1, y1, x2, y2 = x, y, x + w, y + h

#             # Crop the face from the frame
#             face_crop = frame[y1:y2, x1:x2]

#             # Get embedding for the face
#             embedding = DeepFace.represent(img_path=face_crop, model_name='Facenet', detector_backend='opencv', enforce_detection=False)[0]['embedding']

#             # Compute distances
#             distances = np.linalg.norm(np.array(enck) - np.array(embedding), axis=1)
#             matchindex = np.argmin(distances)
#             min_distance = distances[matchindex]

#             name = 'Unknown'
#             category = 'Green'
#             if min_distance <= 0.6:  # Adjusted threshold for DeepFace
#                 name = Names[matchindex].upper()
#                 ids = ''
#                 if name in CriminalNames:
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                     cv2.putText(frame, name, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
#                     os.makedirs(os.path.join(BASE_DIR, 'Recognize/recognized/Criminal'), exist_ok=True)
#                     cv2.imwrite(os.path.join(BASE_DIR, 'Recognize/recognized/Criminal', '{}.jpg'.format(name)), frame)
#                     category = 'Criminal/Red'
#                     ids = IDS[matchindex]
#                     if ids not in namea:
#                         namea.append(ids)
#                         ReportFileEdit(name, category, ids)
#                 elif name in MissingNames:
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
#                     cv2.putText(frame, name, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
#                     os.makedirs(os.path.join(BASE_DIR, 'Recognize/recognized/Missing'), exist_ok=True)
#                     cv2.imwrite(os.path.join(BASE_DIR, 'Recognize/recognized/Missing', '{}.jpg'.format(name)), frame)
#                     category = 'Missing/Yellow'
#                     ids = IDS[matchindex]
#                     if ids not in namea:
#                         namea.append(ids)
#                         ReportFileEdit(name, category, ids)
#             else:
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

#             return [name, category]
#     except Exception as e:
#         print("Error in FRDist: {}".format(e))
#         return ['Unknown', 'Green']
import cv2
import numpy as np
import os
from deepface import DeepFace
from scipy.spatial.distance import cosine
def FRDist(frame, enck, Names):
    detected_name = 'Unknown'
    detected_category = 'Green'
    coords = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
    try:
        # CHANGE 1: Use 'dlib' for high accuracy and efficiency in streaming
        # Dlib provides better face detection accuracy than mtcnn while being memory-efficient
        results = DeepFace.represent(
            img_path=frame,
            model_name='Dlib',
            detector_backend='dlib',  # <--- Changed to dlib for high accuracy and memory efficiency
            enforce_detection=False
        )

        for res in results:
            embedding = res['embedding']
            facial_area = res['facial_area']
            coords = {
                'x': facial_area['x'],
                'y': facial_area['y'],
                'w': facial_area['w'],
                'h': facial_area['h']
            }
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            x1, y1, x2, y2 = x, y, x + w, y + h

            # CHANGE 2: Use Cosine Distance instead of Euclidean
            # Cosine is usually better for Face Verification.
            # We calculate cosine distance for every known encoding manually.
            distances = []
            for known_enc in enck:
                # specific scipy cosine function is safer/easier than numpy manual calc
                d = cosine(known_enc, embedding)
                distances.append(d)
            
            distances = np.array(distances)
            matchindex = np.argmin(distances)
            min_distance = distances[matchindex]

            # DEBUG: Print the distance to help you tune the threshold
            print(f"Match candidate: {Names[matchindex]} | Distance: {min_distance}")

            # CHANGE 3: Cosine Threshold
            # For Facenet + Cosine, 0.40 is a good starting point.
            # If it's still failing, try increasing this to 0.50.
            threshold = 0.40 

            if min_distance <= threshold:
                name = Names[matchindex].upper()
                detected_name = name
                
                # --- Visuals & Saving Logic (Same as before) ---
                if name in CriminalNames:
                    detected_category = 'Criminal/Red'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, f"{name} ({min_distance:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 2)
                    
                    # Saving logic...
                    save_path = os.path.join(BASE_DIR, 'Recognize/recognized/Criminal')
                    os.makedirs(save_path, exist_ok=True)
                    cv2.imwrite(os.path.join(save_path, f'{name}.jpg'), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    
                    # Report logic...
                    ids = IDS[matchindex]
                    if ids not in namea:
                        namea.append(ids)
                        ReportFileEdit(name, detected_category, ids)

                elif name in MissingNames:
                    detected_category = 'Missing/Yellow'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                    cv2.putText(frame, f"{name} ({min_distance:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 2)
                    
                    save_path = os.path.join(BASE_DIR, 'Recognize/recognized/Missing')
                    os.makedirs(save_path, exist_ok=True)
                    cv2.imwrite(os.path.join(save_path, f'{name}.jpg'), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    
                    ids = IDS[matchindex]
                    if ids not in namea:
                        namea.append(ids)
                        ReportFileEdit(name, detected_category, ids)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{name} ({min_distance:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

            else:
                # Unknown
                cv2.rectangle(frame, (x1, y1), (x2, y2), (128, 128, 128), 2)
                # cv2.putText(frame, f"Unknown ({min_distance:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (128, 128, 128), 2)

        return [detected_name, detected_category,coords]

    except Exception as e:
        print(f"Error in FRDist: {e}")
        return ['Unknown', 'Green']
    

def FRDistVideo(frame, enck, Names):
    detected_name = 'Unknown'
    detected_category = 'Green'
    coords = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
    
    try:
        #
        # DeepFace detection (optimized logic remains here...)
        results = DeepFace.represent(
            img_path=frame,
            model_name='Dlib',
            detector_backend='dlib',  # Changed to mtcnn for better accuracy and reasonable memory usage in streaming
            enforce_detection=False
        )

        for res in results:
            # ... (Embedding and Coordinate extraction logic remains same) ...
            embedding = res['embedding']
            facial_area = res['facial_area']
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            x1, y1, x2, y2 = x, y, x + w, y + h
            coords = {'x': x, 'y': y, 'w': w, 'h': h}

            # Distance Calculation Logic
            distances = []
            for known_enc in enck:
                d = cosine(known_enc, embedding)
                distances.append(d)
            
            distances = np.array(distances)
            matchindex = np.argmin(distances)
            min_distance = distances[matchindex]
            threshold = 0.40

            if min_distance <= threshold:
                name = Names[matchindex].upper()
                person_id = IDS[matchindex] # Ensure you have access to IDS list here
                detected_name = name

                # --- Draw Visuals on Frame (Always do this for stream) ---
                color = (0, 255, 0) # Default Green
                if name in CriminalNames:
                    detected_category = 'Criminal/Red'
                    color = (255, 0, 0) # Red
                elif name in MissingNames:
                    detected_category = 'Missing/Yellow'
                    color = (255, 255, 0) # Yellow

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{name} ({min_distance:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)

                # --- OPTIMIZED SAVING ---
                # This line replaces your entire messy saving block.
                # It handles threading, duplicate checking, and directory creation.
                if detected_category != 'Green': # Only save interesting people
                     save_detection_once(frame, name, detected_category, person_id, BASE_DIR)

            else:
                # Unknown Handling
                cv2.rectangle(frame, (x1, y1), (x2, y2), (128, 128, 128), 2)

        return [detected_name, detected_category, coords]

    except Exception as e:
        print(f"Error in FRDist: {e}")
        return ['Unknown', 'Green', coords]
    
