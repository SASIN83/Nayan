# NAYAN: Virtual Police Station

Django-based face recognition system for virtual policing operations with optimized memory usage for streaming applications.

## Features

- Face recognition for missing persons and criminals using DeepFace library
- Real-time video streaming with optimized face detection
- Automatic report generation for detected individuals
- Image gallery for recognized persons
- IP geolocation tracking for recognition events
- Memory-optimized processing for high-resolution video streams

## Recent Optimizations

- **Memory Usage Reduction**: Reduced image processing max_width from 800 to 480 pixels
- **Improved Face Detection**: Switched to dlib detector backend for better accuracy and memory efficiency
- **Updated Dependencies**: Streamlined requirements.txt with current package versions

## Project Structure

- `Nayan/`: Django project root
- `Nayan/Project/`: Face recognition backend (training, recognition, registration)
- `Nayan/Recognize/`: Django app for web interface
- `requirements.txt`: Python dependencies

## Prerequisites

- Python 3.7.9 (recommended for dlib stability)
- Git for version control

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nayan
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If dlib installation fails, download the pre-built wheel:

```bash
# Download from: https://github.com/SASIN83/dlibpreinstalled
pip install dlib-19.19.0-cp37-cp37m-win_amd64.whl
```

### 4. Database Setup

```bash
cd Nayan
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Application

```bash
python manage.py runsslserver ip:port
```

Access the application at `http://<IP>:<PORT>/app`

## Usage

### Training New Faces

1. Place images in the appropriate directory with format: `ID.Name.jpeg`
2. Run training script: `python Project/Train.py`
3. Delete old `.pkl` files before retraining or modify `Train.py` to append

### Recognition

- Upload images through the web interface
- Use video streaming for real-time recognition
- Reports are automatically generated for detected individuals

## Dependencies

- Django >= 3.2.0: Web framework
- deepface >= 0.0.75: Face recognition library
- opencv-python >= 4.5.5.64: Computer vision
- dlib >= 19.22.0: Face detection
- numpy >= 1.21.0: Numerical computing
- scipy >= 1.7.0: Scientific computing
- Pillow >= 8.0.0: Image processing
- tensorflow >= 2.8.0: Machine learning
- keras >= 2.8.0: Neural networks

## Version Control

This project uses Git for version control. Key branches:

- `main`: Stable production code
- `develop`: Development branch

### Common Git Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to repository
git push origin main
```

## Performance Notes

- **Memory Optimization**: Images are resized to max 480px width during processing to prevent memory crashes
- **Face Detection**: Uses dlib backend for optimal balance of accuracy and memory usage
- **Streaming**: Optimized for real-time video processing without excessive memory consumption

## Limitations

- Currently supports single face input only
- Manual training process
- Basic image gallery interface
- Chatbot feature not implemented

## Contributing

Contributions are welcome. Please ensure code follows the existing structure and includes appropriate documentation.
