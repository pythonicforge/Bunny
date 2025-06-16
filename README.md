# Bunny

Bunny is a simple Streamlit web app that allows you to easily change the perspective of objects in your images. Upload an image, select four points on the image, and Bunny will correct the perspective for you. You can then download the corrected image.

<br/>

### Features
- Upload images in JPG, PNG, or JPEG format
- Interactive canvas to select four points for perspective correction
- Real-time perspective transformation using OpenCV
- Download the corrected image
- Reset and select new points as needed

<br/>

### How to Use
1. **Upload an Image**: Click the file uploader and select your image.
2. **Select Four Points**: Click exactly four points on the image in the order: top-left, top-right, bottom-left, bottom-right.
3. **View Result**: The app will automatically correct the perspective and display the result.
4. **Download**: Click the download button to save the corrected image.
5. **Reset**: Use the reset button to select new points if needed.

<br/>

### Requirements
- Python 3.7+
- Streamlit
- streamlit-drawable-canvas
- Pillow
- OpenCV (cv2)
- numpy

Install dependencies with:
```bash
pip install -r requirements.txt
```

<br/>

### Running the App
```bash
streamlit run main.py
```

<br/>

### Deployment
This app is compatible with Streamlit Cloud and other remote servers. If you encounter issues with the image not displaying on the canvas, try resizing your image or check your requirements.

<br/>

### File Structure
- `main.py` - Main application code
- `requirements.txt` - Python dependencies
- `runtime.txt` - (Optional) Python version for deployment

<br/>

### License
MIT License
