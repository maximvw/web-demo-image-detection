from fastapi import FastAPI, File, Response
from PIL import Image
import torch
from io import BytesIO

app = FastAPI()


def load_model():
    model_out = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True).eval()
    return model_out


model = load_model()


def detect(pil_img):
    result = model(pil_img)
    out_img = Image.fromarray(result.render()[0], 'RGB')

    buf = BytesIO()
    out_img.save(buf, format="JPEG")
    byte_img = buf.getvalue()
    return byte_img


@app.get('/')
async def root():
    return 'Hi, Boss'


@app.post('/detect-image')
async def detect_image(image_file: bytes = File()):
    pil_img = Image.open(BytesIO(image_file))
    bytes_result = detect(pil_img)
    return Response(content=bytes_result, media_type="image/png")
