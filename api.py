from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO as yolo
import os
import uuid
import uvicorn
from config import UPLOAD_DIR, YOLO_PATH

app = FastAPI()
model = yolo(YOLO_PATH)


class Info:
    image: UploadFile
    animal_name: str


def check_animal_in_image(image_data, animal_name):
    content = image_data
    filename = f"{str(uuid.uuid4())}.jpg"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)

    results = model(UPLOAD_DIR + filename)
    for result in results:
        for c in result.boxes.cls:
            if model.names[int(c)] == animal_name:
                return True
    return False


@app.post("/check_animal")
async def check_animal(image: UploadFile = File(), animal_name: str = Form()):
    try:
        image_data = await image.read()
        result = check_animal_in_image(image_data, animal_name)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
