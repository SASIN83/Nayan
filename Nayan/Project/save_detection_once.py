import os
import cv2
import threading

# Global set to remember who we have already saved in this session
# This prevents saving the same person 100 times in 10 seconds.
ALREADY_SAVED = set()

def save_detection_once(frame_rgb, name, category, person_id, base_dir):
    """
    Saves the detection image ONLY if this person_id hasn't been saved recently.
    Runs in a separate thread to prevent blocking the video stream.
    """
    global ALREADY_SAVED

    # 1. Check if already saved
    if person_id in ALREADY_SAVED:
        return  # Skip immediately if we already have this person

    # 2. Add to set immediately to block other frames from trying to save
    ALREADY_SAVED.add(person_id)

    # 3. Define the saving worker (So disk I/O doesn't pause the video)
    def _save_worker(img, p_name, p_cat, p_id, b_dir):
        try:
            # Determine folder based on category
            subfolder = 'Unknown'
            if 'Criminal' in p_cat:
                subfolder = 'Criminal'
            elif 'Missing' in p_cat:
                subfolder = 'Missing'
            
            # Construct paths
            directory = os.path.join(b_dir, 'Recognize', 'recognized', subfolder)
            os.makedirs(directory, exist_ok=True)
            
            filename = f"{p_name}_{p_id}.jpg"
            full_path = os.path.join(directory, filename)

            # Convert RGB back to BGR for OpenCV saving
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            # Write to disk
            cv2.imwrite(full_path, img_bgr)

            # Trigger Report Editing (Assuming you have this function)
            # ReportFileEdit(p_name, p_cat, p_id)

        except Exception as e:
            # Optional: Remove from set if save failed so we can try again
            if p_id in ALREADY_SAVED:
                ALREADY_SAVED.remove(p_id)

    # 4. Run the worker in a thread
    t = threading.Thread(target=_save_worker, args=(frame_rgb.copy(), name, category, person_id, base_dir))
    t.daemon = True
    t.start()