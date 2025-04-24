from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/draw-line")
async def draw_red_line(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # 赤線を描く
    cv2.line(img, (50, 50), (300, 50), (0, 0, 255), 5)

    _, encoded_img = cv2.imencode('.jpg', img)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
