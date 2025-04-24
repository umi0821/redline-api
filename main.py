from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import io
import json

app = FastAPI()

@app.post("/draw-lines")
async def draw_red_lines(request: Request, file: UploadFile = File(...)):
    form = await request.form()
    lines_data = form.get("lines")

    try:
        # 文字列だったらパースする（文字列で送られた場合）
        line_data = json.loads(lines_data)
    except:
        # すでに配列ならそのまま（配列で送られた場合）
        line_data = lines_data

    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    for line in line_data:
        start = tuple(line["start"])
        end = tuple(line["end"])
        cv2.line(img, start, end, (0, 0, 255), 3)

    _, encoded_img = cv2.imencode('.jpg', img)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
