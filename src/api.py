from fastapi import FastAPI, File, UploadFile, Response
import cv2 as cv
import numpy as np
from src.segment import run_pipeline

# 1. Initialize the FastAPI app
app = FastAPI(title="Cell Segmentation API", version="1.0.0")


# 2. Health check endpoint (GET request)
# Visiting http://localhost:8000/ in a browser triggers this
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Cell Segmentation API is up and running!"
    }


# 3. Image Segmentation endpoint (POST request)
# Uploading an image file triggers this
@app.post("/segment")
async def segment_cell_image(file: UploadFile = File(...)):
    # Step A: Read the raw bytes uploaded over HTTP
    contents = await file.read()

    # Step B: Convert bytes into an OpenCV image (numpy array)
    np_array = np.frombuffer(contents, np.uint8)
    img = cv.imdecode(np_array, cv.IMREAD_COLOR)

    # Step C: Run your existing Watershed pipeline!
    result = run_pipeline(img)

    # Step D: Encode the segmented OpenCV image back to PNG bytes
    _, encoded_img = cv.imencode(".png", result)

    # Step E: Return the PNG image directly as HTTP response
    return Response(content=encoded_img.tobytes(), media_type="image/png")
