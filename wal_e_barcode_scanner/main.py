from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
async def scan_image(image: UploadFile = File(...)):
    img_bytes = await image.read()
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    barcodes = decode(img)
    for barcode in barcodes:
        if barcode.type == "EAN13":
            return JSONResponse({"barcode": barcode.data.decode()})

    return JSONResponse({"barcode": None})