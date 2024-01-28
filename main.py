from ultralytics import YOLO as yolo
from config import YOLO_PATH, YAML_PATH
import os

# os.environ['KMP_DUPLICATE_LIB_OK']='True'

if __name__ == '__main__':
    eight = 'yolov8n.pt'
    version = YOLO_PATH
    model = yolo(eight)
    model.train(data=YAML_PATH, epochs=20, workers=0)

    print('done')
