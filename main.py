from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS_DB = {}

# Load products from CSV into the PRODUCTS_DB dictionary
def load_products_from_csv():
    with open('productinfo.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            barcode = row["barcode"]
            PRODUCTS_DB[barcode] = {
                "name": row["name"],
                "price": row["price"],
                "selling_price": row["selling_price"],
                "net_weight": row["net_weight"]
            }

load_products_from_csv()

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
