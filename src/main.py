from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, Response
from stereo import *
import cv2
import numpy as np
import base64

app = FastAPI()

@app.post('/decode')
async def _file_upload(
        file: UploadFile = File(...),
):
    content = await file.read()
    nparr = np.fromstring(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    result = decode_stereogram(img)

    img_str = cv2.imencode('.png', result)[1].tostring()
    return Response(img_str, media_type="image/png")
