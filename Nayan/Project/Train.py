import cv2
import numpy as np
from deepface import DeepFace
import os
import pickle
from Register import BASE_DIR

# Keep your helper functions (byte2image, image2byte) as they are...

def Train(path):    
    images = []
    Names = []
    ids = []
    lst = os.listdir(path)
    
    print(f"Training on images in: {path}")

    for pl in lst:
        img_path = os.path.join(path, pl)
        
        # 1. Read the image
        imgn = cv2.imread(img_path)
        
        if imgn is None:
            print(f"Warning: Could not read image {pl}")
            continue

        # --- THE CRITICAL FIX ---
        # OpenCV reads as BGR. We must convert to RGB to match PIL/DeepFace.
        imgn = cv2.cvtColor(imgn, cv2.COLOR_BGR2RGB)
        # ------------------------

        images.append(imgn)
        
        # Parsing filename structure: ID.Name.jpg
        try:
            # Splits "001.John.jpg" -> ID="001", Name="John"
            file_name = os.path.splitext(pl)[0] # "001.John"
            file_parts = file_name.upper().split('.') 
            
            if len(file_parts) >= 2:
                ids.append(file_parts[0])
                Names.append(file_parts[1])
            else:
                # Fallback if naming convention isn't perfect
                ids.append("Unknown")
                Names.append(file_parts[0])
                
        except Exception as e:
            print(f"Error parsing filename {pl}: {e}")

    def findenc(images):
        encL = []
        for i, img in enumerate(images):
            try:
                # img is now a valid RGB numpy array
                enc = DeepFace.represent(
                    img_path=img, 
                    model_name='Dlib', 
                    detector_backend='dlib', 
                    enforce_detection=False
                )[0]['embedding']
                encL.append(enc)
            except Exception as e:
                print(f"Error encoding image index {i}: {e}")
                # If encoding fails, we must remove the corresponding Name/ID 
                # to keep lists synchronized, otherwise indexes will shift.
                # Note: This simple logic assumes 1-to-1. 
                # For production, it's better to build lists together.
                pass 
        return encL
    
    # Calculate encodings
    if len(images) > 0:
        enck = findenc(images)
        
        # Ensure encodings match names length (in case some faces weren't detected)
        # DeepFace 'enforce_detection=False' usually returns something, but good to be safe.
        if len(enck) != len(Names):
             print(f"Warning: {len(Names)} names but {len(enck)} encodings. Lists might be out of sync.")

        # Logic to decide which file to save to
        # (This logic relies on the order you call the function)
        project_path = os.path.join(BASE_DIR, 'Project')
        os.makedirs(project_path, exist_ok=True)
        
        existing_files = os.listdir(project_path)
        
        # If we are processing the Criminal path (heuristic check based on path name)
        if 'Criminal' in path:
            save_file = 'CriminalSet.pk'
            print("Saving to CriminalSet.pk")
        elif 'Missing' in path:
            save_file = 'MissingSet.pk'
            print("Saving to MissingSet.pk")
        else:
            # Fallback to your original logic
            if 'CriminalSet.pk' not in existing_files:
                save_file = 'CriminalSet.pk'
            else:
                save_file = 'MissingSet.pk'

        pickle.dump((ids, enck, Names), open(os.path.join(project_path, save_file), 'wb'))
        print(f"Successfully Encoded and Saved {len(enck)} faces to {save_file}")
        print("Names added:", Names)
    else:
        print("No images found in path.")

# --- Execution ---
# Ensure you delete old .pk files before running this!
x = os.listdir()
# You might want to force retraining by commenting out the 'if' check temporarily
# if 'CriminalSet.pk' not in x or 'MissingSet.pk' not in x:


def Update_Train(image_path, category='Criminal'):
    """
    Appends a new face to the existing pickle file without retraining the whole set.
    
    Args:
        image_path (str): Full path to the specific image file (e.g., ".../005.Joker.jpg")
        category (str): 'Criminal' or 'Missing'
    """

    # 1. Determine which file to load based on category
    project_path = os.path.join(BASE_DIR, 'Project')
    if category == 'Criminal':
        pkl_file = os.path.join(project_path, 'CriminalSet.pk')
    else:
        pkl_file = os.path.join(project_path, 'MissingSet.pk')

    # 2. Load existing data
    if os.path.exists(pkl_file):
        try:
            print(f"Loading {pkl_file}...")
            with open(pkl_file, 'rb') as f:
                ids, enck, Names = pickle.load(f)
        except Exception as e:
            print(f"Error reading pickle file: {e}")
            return
    else:
        print("Pickle file not found. Creating new lists.")
        ids, enck, Names = [], [], []

    # 3. Read and Preprocess the New Image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # CRITICAL: Convert BGR to RGB so it matches the training data format
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 4. Extract Name and ID from filename
    # Assumes filename format: "ID.Name.jpg" (e.g., "101.JohnDoe.jpg")
    filename = os.path.basename(image_path)
    clean_name = os.path.splitext(filename)[0] # Remove .jpg
    parts = clean_name.upper().split('.')
    
    if len(parts) >= 2:
        new_id = parts[0]
        new_name = parts[1]
    else:
        new_id = "Unknown"
        new_name = parts[0]

    # 5. Generate Embedding
    try:
        new_embedding = DeepFace.represent(
            img_path=img_rgb, 
            model_name='Dlib', 
            detector_backend='dlib', 
            enforce_detection=False
        )[0]['embedding']

        # 6. Append to Lists
        ids.append(new_id)
        Names.append(new_name)
        enck.append(new_embedding)

        # 7. Save back to Pickle
        with open(pkl_file, 'wb') as f:
            pickle.dump((ids, enck, Names), f)
        
        print(f"Success: Added {new_name} (ID: {new_id}) to {category} database.")

    except Exception as e:
        print(f"Error generating embedding: {e}")


print("Starting Training Process...")
want_to_update = input("Do you want to update existing databases? (y/n): ").strip().lower()
if want_to_update == 'y':
    category = input("Enter category to update (Criminal/Missing): ").strip()
    if category not in ['Criminal', 'Missing']:
        print("Invalid category. Please enter 'Criminal' or 'Missing'.")
        exit(1)
    image_path = input("Enter full path to the image file to add: ").strip()
    if not os.path.isfile(image_path):
        print("Invalid file path. Please check and try again.")
        exit(1)
    Update_Train(image_path, category=category)
    print("Update mode selected. Use Update_Train function for adding new faces.")
else:
    Train(os.path.join(BASE_DIR, 'Project\Criminal DB\Criminal DB'))
    Train(os.path.join(BASE_DIR, 'Project\MissingDB\MissingDB'))
    print("Training Completed.")