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

# Sample in-memory product database
PRODUCTS_DB = {
    "0123456789012": {
        "name": "Amul Milk 1L",
        "price": "$1.50",
        "selling_price": "$1.20",
        "net_weight": "1L"
    },
    "1234567890128": {
        "name": "Parle-G Biscuit Pack",
        "price": "$0.60",
        "selling_price": "$0.50",
        "net_weight": "120g"
    },
    "8906155430452": {
        "name": "Tata Salt",
        "price": "$0.80",
        "selling_price": "$0.70",
        "net_weight": "1kg"
    }
}

@app.post("/scan")
async def scan_image(image: UploadFile = File(...)):
    img_bytes = await image.read()
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    barcodes = decode(img)
    for barcode in barcodes:
        if barcode.type == "EAN13":
            barcode_data = barcode.data.decode()
            product = PRODUCTS_DB.get(barcode_data)
            return JSONResponse({
                "barcode": barcode_data,
                "product": product  # Will be null if not found
            })

    return JSONResponse({"barcode": None, "product": None})
